FROM ubuntu:18.04

RUN \
    # ---- パッケージのインストール ----
    apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
        tzdata \
        locales \
        less \
        unzip \
        python2.7 \
        mysql-client \
        libaio1 && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    # ---- タイムゾーンとロケールの設定 ----
    ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    sed -i -E 's/# (ja_JP.UTF-8)/\1/' /etc/locale.gen && \
    locale-gen && \
    # ---- ユーザーとグループの追加 ----
    groupadd -r docker && \
    useradd -r -g docker docker

# ---- sqlplusのインストール ----
COPY docker/local/db-client/sqlplus/instantclient-basic-linux.x64-19.11.0.0.0dbru.zip   /opt/oracle/
COPY docker/local/db-client/sqlplus/instantclient-sqlplus-linux.x64-19.11.0.0.0dbru.zip /opt/oracle/

WORKDIR /opt/oracle/

RUN unzip instantclient-basic-linux.x64-19.11.0.0.0dbru.zip && \
    unzip instantclient-sqlplus-linux.x64-19.11.0.0.0dbru.zip && \
    echo "/opt/oracle/instantclient_19_11" > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ldconfig

# ---- アプリケーションの配置 ----
USER docker

ENV TZ="Asia/Tokyo" \
    LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8"

COPY --chown=docker:docker db-client                     /app/db-client
COPY --chown=docker:docker docker/local/db-client/config /app/config

# ---- アプリケーションの起動 ----
WORKDIR /app/
CMD ["/bin/bash"]
