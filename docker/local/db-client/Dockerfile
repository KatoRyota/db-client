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
        libaio1 \
        curl && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    # ---- タイムゾーンとロケールの設定 ----
    ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    sed -i -E 's/# (ja_JP.UTF-8)/\1/' /etc/locale.gen && \
    locale-gen && \
    # ---- ユーザーとグループの追加 ----
    groupadd -g 61000 docker && \
    useradd -m -g docker -u 61000 docker && \
    # ---- pipのインストール ----
    curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py && \
    python2.7 get-pip.py && \
    python2.7 -m pip install --upgrade pip setuptools

# ---- sqlplusのインストール ----
COPY docker/local/db-client/sqlplus/instantclient-basic-linux.x64-19.11.0.0.0dbru.zip   /opt/oracle/
COPY docker/local/db-client/sqlplus/instantclient-sqlplus-linux.x64-19.11.0.0.0dbru.zip /opt/oracle/

WORKDIR /opt/oracle/

RUN unzip instantclient-basic-linux.x64-19.11.0.0.0dbru.zip && \
    unzip instantclient-sqlplus-linux.x64-19.11.0.0.0dbru.zip && \
    echo "/opt/oracle/instantclient_19_11" > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ldconfig

# ---- アプリケーションのデプロイ ----
USER docker

ENV TZ="Asia/Tokyo" \
    LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8" \
    PATH=/home/docker/.local/bin:${PATH}

COPY --chown=docker:docker . /app/db-client

WORKDIR /app/db-client/

RUN python2.7 setup.py bdist_wheel && \
    python2.7 -m pip install --user dist/db_client-0.0.1-py2-none-any.whl

CMD ["/bin/bash"]
