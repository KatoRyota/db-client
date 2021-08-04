# db-client

db-clientは、データベースにSQLを発行して、各種操作を行う為の、コマンドラインツールです。  
内部でsqlplusやmysqlを呼び出しています。

Table形式での出力や、CSV形式での出力を行うことができます。

---- Table形式 ----

```text
+-----------+-------------+-------------+
|ID         |NAME         |TYPE         |
+-----------+-------------+-------------+
|ID-000-0000|NAME-000-0000|TYPE-000-0000|
+-----------+-------------+-------------+
|ID-111-1111|NAME-111-1111|TYPE-111-1111|
+-----------+-------------+-------------+

2行が選択されました。
```

---- CSV形式 ----

```text
ID-000-0000,NAME-000-0000,TYPE-000-0000
ID-111-1111,NAME-111-1111,TYPE-111-1111
```

# Requirement

* python 2.6 <= 2.7
* sqlplus
* mysql

# Getting Started

以下をご確認下さい。

* [docker/local/README.md](docker/local/README.md)

# Installation

以下のようにdb-clientをダウンロードして下さい。

```shell
cd ~/repo/
git clone https://github.com/KatoRyota/db-client.git
```

以上です。

# Usage

設定ファイル(`application.conf`)に、DBの接続先情報を設定して下さい。  
ターミナルのエンコーディングに、utf-8を設定して下さい。  
ターミナルの文字フォントに、MSゴシックなどの等幅フォントを設定して下さい。  
ターミナルの環境変数[`PYTHONIOENCODING`]に、`utf-8`をセットして下さい。

以下に使い方の一例を記載します。

```shell
cd ${APP_ROOT_DIR}

python -m dbclient 2>&1 <<EOF | less -S
select * from employee;
EOF
```

上記コマンドがエラーになる場合は、以下を試してみて下さい。

```shell
cd ${APP_ROOT_DIR}

python -m dbclient.__main__ 2>&1 <<EOF | less -S
select * from employee;
EOF
```

指定可能なオプションは、以下のコマンドでご確認下さい。

```shell
python -m dbclient -h
```
