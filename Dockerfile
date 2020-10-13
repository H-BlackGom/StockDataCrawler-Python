FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
    language-pack-ko \
    fonts-nanum

## 언어 설정
RUN locale-gen ko_KR.UTF-8
ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

# TimeZone 설정
ENV TZ Asia/Seoul
RUN echo $TZ > /etc/timezone && \
    apt-get update && apt-get install -y tzdata && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

RUN sed -i 's/archive.ubuntu.com/kr.archive.ubuntu.com/g' /etc/apt/sources.list
RUN apt-get update
RUN apt-get update && apt-get install -y curl software-properties-common python-software-properties git

## install python 3.6
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.6 python3-pip

COPY ./ /Collectors
RUN chmod 0777 /Collectors/start.sh

RUN python3.6 -m pip install pip --upgrade && \
    pip install -r /Collectors/requirements.txt

ADD ./Utils/crontab /etc/cron.d/hello-cron
RUN chmod 0644 /etc/cron.d/hello-cron

# Cron 실행
CMD cron -f
