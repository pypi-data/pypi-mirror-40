import os
import docker
import wget
import argparse
from sys import platform as _platform
from etc42.etc42 import __version__
# -------------------------#
# get_path function

def get_path(file_name):
    """Get the full path of file in configuration directory.

    :param file_name: Name of the file.
    :return: Full path of configuration file.

    :Example:

    get_path("my_conf.conf") # -> /python/package/path/my_conf.conf
    """

    return os.path.join(os.path.dirname(__file__), file_name)

# -------------------------- #
# get_directory_path function

def get_directory_path():
    """
    Get the full path of directory python package.
    :return: path of directory file.
    :Example:
    get_directory_path() # -> /python/package/path
    """

    return os.path.dirname(__file__)

# -------------------------- #
# get_args_from_file function

def get_args_from_file(file_name, args):
    """
    Get arguments value from configuration file.

    :param file_name: name of the configuration file
    :param args: object (ex. retrieve from argparse module)

    Get arguments value from configuration file. Value has to be formatted as
    ``option = string``. To comment use ``#``.
    The function modifies every ``None`` args attribue.
    The function add new args attribute.

    :Example:

    In ``my_conf.conf`` file:
    arg1 = 2
    arg2 = foo

    class MyCls():
        arg1=1

    args = MyCls()
    get_args_from_file("my_conf.conf",args)

    args.arg1 # -> 1
    args.arg2 # -> foo
    """

    with open(file_name, 'r') as ff:
        lines = ff.readlines()
    for line in lines:
        try:
            key, value = line.replace('\n', '').split('#')[0].split("=")
        except ValueError:
            continue
        try:
            if getattr(args, key.strip()) is None:
                setattr(args, key.strip(), value.strip())
        except AttributeError:
            setattr(args, key.strip(), value.strip())

# ---------------------------- #
# update_version_from_file

def update_version_from_file(file_name, new_val):
    """
    Update etc42 version number from configuration file.

    :param file_name: name of the configuration file
    :param new_val: etc42 version number

    """

    list_lines = []

    with open(file_name, 'r') as ff:
        lines = ff.readlines()

    for line in lines:
        try:
            key, value = line.replace('\n', '').split('#')[0].split("=")

            if key == 'etc42_version ':
                s = line.replace(value, new_val)
                list_lines.append(s)
            else:
                list_lines.append(line)

        except ValueError:
            continue

    ff.close()

    with open(get_path(".temp.conf"), 'w') as gg:
        for line in list_lines:
            try:
                gg.write(line)
            except Exception as e:
                print('=> Error while updating : ' + str(e))
                return False

    gg.close()
    os.remove(file_name)
    os.rename(get_path('.temp.conf'), file_name)

    return True

# --------------------- #
# get_jar_etc42 function

def get_jar_etc42(etc42_jar, etc42_url):
    """
    Upload the etc42 jar
    :param etc42_jar: Name of the jar version of etc42.
    :param etc42_url: Url of etc42.
    :return: True or False, success or failure of uploading operation.

    :Example:
    get_jar_etc42("etc42-1.0.0.11.jar",etc42_url) # -> True (uploading with success etc42-1.0.0.11.jar)
                                                  # -> False (Failure)
    """

    print('- Download of {} in progress ...'.format(etc42_jar))

    try:

        print('=> Connection to cesam.lam.fr')

        url = etc42_url + etc42_jar
        wget.download(url, get_path(etc42_jar))

        print('')
        print('=> Full {} download \n'.format(etc42_jar))
        return True

    except Exception as e:
        print('=> Error while downloading : ' + str(e))
        return False

# ------------------------ #
# search_jar_update

def search_jar_update(etc42_url):
    """
    Get the last jar version
    :param etc42_url: Url of etc42.
    :return: version number_version
    """

    os.system("curl -s " + etc42_url + " | awk -F'>' '/ETC-Jar/{print $7, $10}' > .temp")

    if _platform == "darwin": #for mac os
        os.system("sed -Ee 's/<\/a/ /g' .temp | awk -F'  ' '{print$2,$1}' > .temp2")
    else:
        os.system("sed -re 's/<\/a/ /g' .temp | awk -F'  ' '{print$2,$1}' > .temp2")


    version=os.popen("sort -r .temp2 | head -1 | awk '{print $3}'").readlines()
    number_version=version[0][8:].replace('.jar','').rstrip()

    return version[0].rstrip(), number_version

# ------------------------ #
# get_image_etc42 function

def get_image_etc42(client, etc42_version):
    """
    Get the docker image etc42 image_etc42-(etc42_version)

    :param client: Client docker.
    :param etc42_version: Number of etc42 version.

    :return: True or False, if docker image etc42 exist or not.

    :Example:
    get_image_etc42(client,"1.0.0.11") # -> True (image_etc42-1.0.0.11 exist)
                                        # -> False (image_etc42-1.0.0.11 not exist)
    """

    image_name = 'image_etc42-' + etc42_version + ':latest'

    try:
        result = client.images.get(image_name)
        return True

    except Exception as e:
        return False

# ------------- #
# build function

def build(client, etc42_version, etc42_jar):
    """
    Build the docker image etc42 image_etc42-(etc42_version)

    :param client: Client docker.
    :param etc42_version: Number of etc42 version.
    :param etc42_jar: etc42 jar.

    :return: True or False, success or failure of building operation.

    :Example:
    build(client,"1.0.0.11", "ETC-Jar-1.0.0.11.jar") # -> True (Building with success image_etc42-1.0.0.11)
                                        # -> False (Failure)
    """

    print('- Creating the etc42-{} docker image in progress ...'.format(etc42_version))

    try:
        image, log = client.images.build(
            path = get_directory_path(),
            dockerfile = 'Dockerfile',
            tag = 'image_etc42-' + etc42_version,
            buildargs = {
                'username' : os.environ['USER'],
                'uidval' : str(os.getuid()),
                'etc42_jar' : etc42_jar,
                'home' : "/home/" + os.environ['USER'],
                },
            rm = True
            )

        print('=> creating the etc42-{} docker image successfully \n'.format(etc42_version))
        return True

    except Exception as e:
        print('type error: ' + str(e))
        return False

# ------------- #
# remove function

def remove(client, etc42_version):
    """
    remove the docker image etc42 image_etc42-(etc42_version)

    :param client: Client docker.
    :param etc42_version: Number of etc42 version.

    :return: True or False, success or failure of removing operation.

    :Example:
    remove_image_etc42(client,"1.0.0.11") # -> True (Removing with success image_etc42-1.0.0.11)
                                        # -> False (Failure)
    """

    print('- Removing the etc42-{} docker image in progress ...'.format(etc42_version))

    try:
        client.images.remove(
            image = 'image_etc42-' + etc42_version
            )

        print('=> removing the etc42-{} docker image successfully \n'.format(etc42_version))
        return True

    except Exception as e:
        print('type error: ' + str(e))
        return False

# ----------- #
# run function

def run(client, etc42_version, etc42_jar):
    """
    run the docker container with docker image etc42

    :param client: Client docker.
    :param etc42_version: Number of etc42 version.
    :param etc42_jar: etc42 jar.
    """

    print('- Container construction and launch in progress ... \n')

    if 'SAMP_HUB' in os.environ:
        val_samp_hub = os.environ['SAMP_HUB']
    else:
        val_samp_hub = os.environ['HOME'] + os.environ['USER'] + "/.samp"

    client.containers.run(
        image = 'image_etc42-' + etc42_version,
        name = 'container_etc42-' + etc42_version,
        network = 'host',
        environment = {
            'DISPLAY' : os.environ['DISPLAY'],
            'USER' : os.environ['USER'],
            'HOME' : os.environ['HOME'],
            'SAMP_HUB' : val_samp_hub
            },
        volumes = {
            '/tmp/.X11-unix' : {'bind' : '/tmp/.X11-unix', 'mode' : 'rw'},
            os.environ['HOME'] : {'bind' : os.environ['HOME'], 'mode' : 'rw'}
            },
        command = 'java -jar /var/etc42/' + etc42_jar,
        remove = 'true')

# ----------- #
# run function
# for mac os

def run_mac(client, etc42_version, etc42_jar):
    """
    run the docker container with docker image etc42
    (run function for mac os)

    :param client: Client docker.
    :param etc42_version: Number of etc42 version.
    :param etc42_jar: etc42 jar.
    """

    print('- Container construction and launch in progress ... \n')

    if 'SAMP_HUB' in os.environ:
        val_samp_hub = os.environ['SAMP_HUB']
    else:
        val_samp_hub = '/home/' + os.environ['USER'] + "/.samp"

    client.containers.run(
        image = 'image_etc42-' + etc42_version,
        name = 'container_etc42-' + etc42_version,
        network = 'host',
        environment = {
            'DISPLAY' : 'host.docker.internal:0',
            'USER' : os.environ['USER'],
            'HOME' : os.environ['HOME'],
            'SAMP_HUB' : val_samp_hub
            },
        volumes = {
            '/tmp/.X11-unix' : {'bind' : '/tmp/.X11-unix', 'mode' : 'rw'},
             '/Users/' + os.environ['USER'] : {'bind' : '/home/' + os.environ['USER'], 'mode' : 'rw'}
            },
        command = 'java -jar /var/etc42/' + etc42_jar,
        remove = 'true')

# ------------ #
# main function

def main():
    """
    etc42 entry point.
    Parse arguments and call the build()
    and run() functions
    """

    # ----------------------------- #
    # --- section etc42 version --- #
    # ----------------------------- #

    parser = argparse.ArgumentParser()

    parser.add_argument("-i","--infos", help="give informations about versions available on cesam server",action="store_true")
    parser.add_argument("-b","--build", metavar='VERSION', help="build etc42 image with selected version number")
    parser.add_argument("--select", metavar='VERSION', help="run etc42 with selected version number")
    parser.add_argument("-u","--update", help="update etc42 image version",action="store_true")
    parser.add_argument("-rm","--remove", nargs=1, help="remove etc42 image with selected version")
    parser.add_argument("-v","--version", help="give etc42 current version number",action="store_true")

    args = parser.parse_args()
    variable = vars(args)
    get_args_from_file(get_path('etc42.conf'), args)

    etc42_url = args.etc42_url
    etc42_version = args.etc42_version
    etc42_jar = 'ETC-Jar-' + etc42_version + '.jar'

    client = docker.from_env()

    select_argument=False

    # ------------args: infos-------------#
    if args.infos:

        select_argument=True
        print("")
        print("-------------------------------------------------------------------")
        print("            etc42 versions available on :")
        print("")
        os.system("echo '\033[31m- CeSAM server : '" + args.etc42_url + "'\033[31m'")
        os.system("echo '\033[32m- Localhost\033[0m'")
        print("-------------------------------------------------------------------")
        print("")

        os.system("curl -s " + etc42_url + " | awk -F'>' '/ETC-Jar/{print $7, $10}' > .temp")
        if _platform == "darwin": #for mac os
            os.system("sed -Ee 's/<\/a/ /g' .temp | awk -F'  ' '{print$2,$1}' > .temp2")
        else:
            os.system("sed -re 's/<\/a/ /g' .temp | awk -F'  ' '{print$2,$1}' > .temp2")


        list_jar=os.popen("sort -r .temp2 | awk '{print $3}'").readlines()

        os.system("rm .temp")
        os.system("rm .temp2")

        for jar in list_jar:
            number_version=jar[8:].replace('.jar','').rstrip()

            if number_version == etc42_version:
                os.system("echo '   \033[32m *\033[0m \033[31m'" + number_version + "'\033[0m'")
            else:
                os.system("echo '   \033[31m   '" + number_version + "'\033[0m'")

        print("-------------------------------------------------------------------")
        print("")

        return 0

    # ------------args: build-------------#
    if args.build:

        select_argument=True
        os.system("curl -s " + etc42_url + " | awk -F'>' '/ETC-Jar/{print $7, $10}' > .temp")

        if _platform == "darwin": #for mac os
            os.system("sed -Ee 's/<\/a/ /g' .temp | awk -F'  ' '{print$2,$1}' > .temp2")
        else:
            os.system("sed -re 's/<\/a/ /g' .temp | awk -F'  ' '{print$2,$1}' > .temp2")

        list_jar=os.popen("sort -r .temp2 | awk '{print $3}'").readlines()
        present=os.popen("sort -r .temp2 | awk '{print $3}' | grep " + args.build).readlines()

        os.system("rm .temp")
        os.system("rm .temp2")


        if len(present) == 0:

            print('')
            print('------------------------------------')
            print('')
            print("You must select an existing version")
            print("   available on the CeSAM server   ")
            print('')
            print('To see the available version(s):')
            print('')
            print("Please make etc42 -i OR --infos")
            print('')
            print('------------------------------------')
            print('')
            return 0

        else:

            etc42_jar = 'ETC-Jar-' + args.build + '.jar'
            etc42_version = args.build
            etc42_url = args.etc42_url

            print('- Searching for the current etc42-{} docker image ...'.format(etc42_version))

            if get_image_etc42(client, etc42_version) is True:

                result_first = remove(client, etc42_version)

            else:
                print('=> The etc42-{} docker image does not exist \n'.format(etc42_version))
                result_first = True

            if result_first is True:
                print('- Searching for the current {} ...'.format(etc42_jar))
                if os.path.isfile(get_path(etc42_jar)):
                    print('=> The {} already exist \n'.format(etc42_jar))
                    result_telechargement = True
                else:
                    print('=> The {} does not exist \n'.format(etc42_jar))
                    result_telechargement = get_jar_etc42(etc42_jar, etc42_url)

                if result_telechargement:
                    result_image = build(client, etc42_version, etc42_jar)
                    os.system("rm " + get_path(etc42_jar))

                else:
                    print('=> Error while downloading of {}'.format(etc42_jar))
            else:
                print('=> Error while removing of image_etc42-{}'.format(etc42_version))

        return 0

    # ------------args: update-------------#
    if args.update:

        select_argument=True
        old_etc42_version=etc42_version
        old_etc42_jar=etc42_jar

        new_etc42_jar,new_etc42_version = search_jar_update(etc42_url)

        if new_etc42_version != old_etc42_version:
            print("=> An update is available")
            print("- new update version:{}".format(new_etc42_version))
            result_telechargement = get_jar_etc42(new_etc42_jar, etc42_url)
            if result_telechargement:
                result_image = build(client, new_etc42_version, new_etc42_jar)
                os.system("rm " + get_path(new_etc42_jar))
                if result_image is True:
                    result_update=update_version_from_file(get_path('etc42.conf'), new_etc42_version)
                    if result_update is True:
                        print("=> Update of configuration file ok")
                    else:
                        print('=> Error while updating of configuration file ')


            else:
                print('=> Error while downloading of {}'.format(new_etc42_jar))

        else:

            print('')
            print('------------------------------------')
            print('')
            print("- ETC42 is up to date")
            print('- etc42 version: {}'.format(new_etc42_version))
            print('')
            print('------------------------------------')


        os.system("rm .temp")
        os.system("rm .temp2")

        return 0;
    # ------------args: remove-------------#
    if args.remove:
        select_argument=True
        result_remove = remove(client, args.remove[0])
        return 0

    # ------------args: version-------------#
    if args.version:

        select_argument=True
        print("etc42 python program version:{}".format(__version__))
        return 0

    # ------------args: select-------------#
    if args.select:

        # ---------------- #
        true_version = False

        os.system("curl -s " + etc42_url + " | awk -F'>' '/ETC-Jar/{print $7, $10}' > .temp")
        if _platform == "darwin": #for mac os
            os.system("sed -Ee 's/<\/a/ /g' .temp | awk -F'  ' '{print$2,$1}' > .temp2")
        else:
            os.system("sed -re 's/<\/a/ /g' .temp | awk -F'  ' '{print$2,$1}' > .temp2")

        list_jar=os.popen("sort -r .temp2 | awk '{print $3}'").readlines()

        os.system("rm .temp")
        os.system("rm .temp2")

        for jar in list_jar:
            number_version=jar[8:].replace('.jar','').rstrip()

            if number_version == args.select:
                true_version = True

        # ---------------- #
        if true_version is True:
            select_argument=True
            etc42_jar = 'ETC-Jar-' + args.select + '.jar'
            etc42_version = args.select
        else:
            print('')
            print('------------------------------------')
            print('')
            print("You must select an existing version")
            print("   available on the CeSAM server   ")
            print('')
            print('To see the available version(s):')
            print('')
            print("Please make etc42 -i OR --infos")
            print('')
            print('------------------------------------')
            print('')
            return 0


    # --------------------------------------- #
    if select_argument is False:
            if args.etc42_version == '?': #case etc42 version default value
                new_etc42_jar,new_etc42_version = search_jar_update(etc42_url)
                result_update=update_version_from_file(get_path('etc42.conf'), new_etc42_version)
                args = parser.parse_args()
                variable = vars(args)
                get_args_from_file(get_path('etc42.conf'), args)
                etc42_url = args.etc42_url
                etc42_version = args.etc42_version
                etc42_jar = 'ETC-Jar-' + etc42_version + '.jar'

    # --------------------------------------- #
    print('')
    print('------------------------------------')
    print(' Universal Exposure Time Calculator ')
    print('               ETC42                ')
    print('')
    print('- etc42 version: {}'.format(etc42_version))
    print('------------------------------------')

    etc42_last_jar,etc42_last_number_version = search_jar_update(etc42_url)
    if etc42_last_number_version != etc42_version:

        print('')
        print('========================================')
        print('YOU ARE NOT USING THE LAST ETC42 VERSION')
        print('========================================')
        print('')
        print('=> A new ETC42 version is available:{}'.format(etc42_last_number_version))
        print('')
        print('COMMAND TO UPDATE ETC42 VERSION:')
        print('')
        print('=> etc42 -u OR --update')
        print('------------------------------------')
        print('')
        print('')
        os.system("sleep 5")


    else:
        #case no update

        print('')
        print('------------------------------------')
        print('')



    os.system("rm .temp")
    os.system("rm .temp2")

    # ----------------------------------------------- #
    # ---  section etc42 docker image management  --- #
    # ----------------------------------------------- #

    #client = docker.from_env()

    print('- Searching for the current etc42-{} docker image ...'.format(etc42_version))

    if get_image_etc42(client, etc42_version) is False:

        print('=> The etc42-{} docker image does not exist \n'.format(etc42_version))

        # --- etc42-[version].jar download --- #
        print('- Searching for the current {} ...'.format(etc42_jar))

        if os.path.isfile(get_path(etc42_jar)):
            print('=> The {} already exist \n'.format(etc42_jar))
            result_telechargement = True
        else:
            print('=> The {} does not exist \n'.format(etc42_jar))
            result_telechargement = get_jar_etc42(etc42_jar, etc42_url)
        # ------------------------------------ #

        # --- etc42-[version] image construction ----- #
        if result_telechargement:
            result_image = build(client, etc42_version, etc42_jar)
            os.system("rm " + get_path(etc42_jar))
        else:
            print('=> Error while downloading of {}'.format(etc42_jar))

    else:
        print('=> The etc42-{} docker image already exist \n'.format(etc42_version))
        result_image = True
        # ------------------------------------------- #

    # --------------------------------------------------- #
    # ---  section etc42 docker container management  --- #
    # --------------------------------------------------- #

    if result_image :
        if _platform == "darwin": #for mac os

            os.system('open -a XQuartz')
            os.system('xhost +')
            run_mac(client, etc42_version, etc42_jar)
            os.system('xhost -')

        elif _platform == "linux" or _platform == "linux2": #for linux os

            os.system('xhost +')
            run(client, etc42_version, etc42_jar)
            os.system('xhost -')

        else:
            #TODO make version for windows
            print('=> actually no version for WINDOWS')

    else:
        print('=> Error while building of {} docker image'.format(etc42_jar))

    # --------------------------------------- #

    print('=> End of etc42 program')
    print('')
