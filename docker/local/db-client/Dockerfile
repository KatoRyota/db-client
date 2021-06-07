FROM ubuntu:18.04

VOLUME ["/sys/fs/cgroup"]

WORKDIR /root

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update

# ---- タイムゾーンの設定 ----
RUN apt install -y tzdata
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
RUN dpkg-reconfigure --frontend noninteractive tzdata
ENV TZ="Asia/Tokyo"

# ---- ロケールの設定 ----
RUN apt install -y locales
RUN locale-gen ja_JP.UTF-8
ENV LANG="ja_JP.UTF-8"
ENV LANGUAGE="ja_JP:ja"
ENV LC_ALL="ja_JP.UTF-8"

# ---- lessのインストール ----
RUN apt install -y less

# ---- wgetのインストール ----
RUN apt install -y wget

# ---- unzipのインストール ----
RUN apt install -y unzip

# ---- Python 2.7のインストール ----
RUN apt install -y python2.7

# ---- sqlplusのインストール ----
COPY ./sqlplus/instantclient-basic-linux.x64-19.11.0.0.0dbru.zip /opt/oracle/
COPY ./sqlplus/instantclient-sqlplus-linux.x64-19.11.0.0.0dbru.zip /opt/oracle/
WORKDIR /opt/oracle
RUN unzip instantclient-basic-linux.x64-19.11.0.0.0dbru.zip
RUN unzip instantclient-sqlplus-linux.x64-19.11.0.0.0dbru.zip
RUN apt install -y libaio1
RUN echo "/opt/oracle/instantclient_19_11" > /etc/ld.so.conf.d/oracle-instantclient.conf
RUN ldconfig

CMD ["/bin/bash"]
