FROM ubuntu:16.04
FROM java:8

ARG uidval
ARG username
ARG etc42_jar
ARG home

RUN mkdir /var/etc42

RUN useradd -r -u $uidval -d $home $username

USER $username

WORKDIR $home

ADD $etc42_jar /var/etc42/
