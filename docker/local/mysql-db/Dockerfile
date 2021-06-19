FROM mysql:8.0.25

RUN \
    # ---- パッケージのインストール ----
    apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
        tzdata \
        locales \
        less  && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    # ---- タイムゾーンとロケールの設定1 ----
    ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    sed -i -E 's/# (ja_JP.UTF-8)/\1/' /etc/locale.gen && \
    locale-gen && \
    # ---- ユーザーとグループの追加 ----
    groupadd -r docker && \
    useradd -r -g docker docker

# ---- ユーザーの変更 ----
USER docker

ENV TZ="Asia/Tokyo" \
    LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8"

# ---- アプリケーションの起動 ----
CMD ["mysqld"]
