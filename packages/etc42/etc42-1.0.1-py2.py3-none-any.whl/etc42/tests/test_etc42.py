"""
File: etc42/tests/test_etc42.py
Created on: 30/11/18
Author: LAM ETC developers
"""
import pytest
import os.path
import tempfile
import threading
import time
import argparse
import docker
from io import BytesIO
from etc42.etc42.etc42 import *

def test_get_args_from_file():
    """
    The "test_get_args_from_file" function.
    This function tests feature of retrieving argument value from
    configuration file
    """
    import tempfile
    fp1 = tempfile.NamedTemporaryFile()
    conf_file = fp1.name
    with open(conf_file, 'w') as cf:
        cf.write('arg1 = 4\n')
        cf.write('arg2 = foo2 foo2\n')
        cf.write('arg3 = foo3 # test\n')
        cf.write('arg4 = # foo4\n')
        cf.write('arg5 # = foo5\n')
        cf.write('#arg6 = foo6')
        cf.write('arg7 arg7 = foo7\n')
    class MyCls():
        arg1 = "2"
    args = MyCls()
    get_args_from_file(conf_file, args)
    assert args.arg1 == "2"
    assert args.arg2 == "foo2 foo2"
    assert args.arg3 == "foo3"
    assert args.arg4 == ""
    with pytest.raises(AttributeError):
        getattr(args, "arg5")
    with pytest.raises(AttributeError):
        getattr(args, "arg6")
    with pytest.raises(AttributeError):
        getattr(args, "arg7")
    fp1.close()

def test_get_path():
    """
    The "test_get_path" function.
    This function tests features concerning configuration directory.
    """
    assert os.path.exists(get_path("."))
    assert not(os.path.exists(get_path("foo.txt")))

def test_get_jar_etc42():
    """
    The "test_get_jar_etc42" function.
    This function tests features of downloading etc42 jar.
    """
    class MyCls():
        url = 'http://cesam.lam.fr/Apps/ETC/webstart/'
        version = '1.0.0.11'
        url_false = 'http://site.fr'
        version_false = '11'

    args = MyCls()

    file_jar = 'ETC-Jar-' + args.version + '.jar'
    file_jar_false = 'file' + args.version_false + '.jar'
    url = args.url
    url_false = args.url_false

    res0 = get_jar_etc42(file_jar_false, url)
    res1 = get_jar_etc42(file_jar, url_false)
    res2 = get_jar_etc42(file_jar_false, url_false)
    res3 = get_jar_etc42(file_jar, url)

    assert res0== False #test bad file
    assert res1== False #test bad url
    assert res2 == False #test bad file and bad url
    assert res3 == True #test good file and exist url

def test_get_image_etc42():
    """
    The "test_get_image_etc42" function.
    This function tests features of getting etc42 image.
    """

    # --- fileobject creation for test --- #
    dockerfile = '''
    FROM alpine:latest
    '''
    f = BytesIO(dockerfile.encode('utf-8'))
    # ------------------------------------ #

    client = docker.from_env()
    version = 'test-1.0'


    image_test=client.images.build(
            fileobj=f,
            tag = 'image_etc42-' + version,
            rm = True
            )

    res0 = get_image_etc42(client,version)
    res1 = get_image_etc42(client,"version-false")

    assert res0 == True #test exist image
    assert res1 == False #test non-exist image


def test_build():
    """
    The "test_run" function.
    This function tests the docker image etc42 run.
    """

    client = docker.from_env()
    version = '1.0.0.11'
    jar = 'etc42-1.0.0.11.jar'
    my_image= build(client, version, jar)

    res = get_image_etc42(client, version)
    assert res == True
