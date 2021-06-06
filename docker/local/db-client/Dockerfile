FROM ubuntu:18.04

VOLUME ["/sys/fs/cgroup"]

WORKDIR /root

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update

# タイムゾーンの設定
RUN apt install -y tzdata
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
RUN dpkg-reconfigure --frontend noninteractive tzdata
ENV TZ="Asia/Tokyo"

# ロケールの設定
RUN apt install -y locales
RUN locale-gen ja_JP.UTF-8
ENV LANG="ja_JP.UTF-8"
ENV LANGUAGE="ja_JP:ja"
ENV LC_ALL="ja_JP.UTF-8"

# lessのインストール
RUN apt install -y less

# wgetのインストール
RUN apt install -y wget

# Python 2.7のインストール

# sqlplusのインストール

CMD ["/bin/bash"]
