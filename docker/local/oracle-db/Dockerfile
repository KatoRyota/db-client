FROM oracle/database:18.4.0-xe

RUN \
    # ---- パッケージのインストール ----
    yum update -y && \
    yum install -y \
        less && \
    yum reinstall -y glibc-common && \
    yum clean all && \
    # ---- タイムゾーンとロケールの設定 ----
    ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8 && \
    # ---- ユーザーとグループの追加 ----
    groupadd -g 61000 docker && \
    useradd -m -g docker -u 61000 docker

# ---- アプリケーションのデプロイ ----
ENV TZ="Asia/Tokyo" \
    LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8"

CMD exec $ORACLE_BASE/$RUN_FILE
# CMD ["/bin/bash"]
