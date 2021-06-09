FROM ubuntu:18.04

WORKDIR /root/

# ---- パッケージのインストール ----
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
        tzdata \
        locales \
        less \
        unzip \
        python2.7 \
        libaio1 && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# ---- タイムゾーンとロケールの設定 ----
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    locale-gen ja_JP.UTF-8

ENV TZ="Asia/Tokyo" \
    LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8"

# ---- sqlplusのインストール ----
COPY ./sqlplus/instantclient-basic-linux.x64-19.11.0.0.0dbru.zip /opt/oracle/
COPY ./sqlplus/instantclient-sqlplus-linux.x64-19.11.0.0.0dbru.zip /opt/oracle/

WORKDIR /opt/oracle/

RUN unzip instantclient-basic-linux.x64-19.11.0.0.0dbru.zip && \
    unzip instantclient-sqlplus-linux.x64-19.11.0.0.0dbru.zip && \
    echo "/opt/oracle/instantclient_19_11" > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ldconfig

WORKDIR /app/

CMD ["/bin/bash"]
