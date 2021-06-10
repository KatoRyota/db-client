# db-client

db-clientは、データベースにSQLを発行して、各種操作を行う為の、Linux用コマンドラインツールです。  
内部でsqlplusやmysqlを呼び出しています。

Table形式での出力や、CSV形式での出力を行うことができます。

---- Table形式 ----

```text
TODO
```

---- CSV形式 ----

```text
TODO
```

# Requirement

* python 2.6 <= 2.7
* sqlplus
* mysql

# Getting Started

以下をご確認下さい。

* [docker/local/README.md](docker/local/README.md)

# Installation

TODO

# Usage

設定ファイル(`application.conf`)に、DBの接続先情報を設定して下さい。  
ターミナルのエンコーディングに、utf-8を設定して下さい。  
ターミナルの文字フォントに、MSゴシックなどの等幅フォントを設定して下さい。  
ターミナルの環境変数[`PYTHONIOENCODING`]に、`utf-8`をセットして下さい。

以下に使い方の一例を記載します。

```shell
cd ${APP_ROOT_DIR}

python -m db-client 2>&1 <<EOF | less -S
select * from employee;
EOF
```

指定可能なオプションは、以下のコマンドでご確認下さい。

```shell
python -m db-client -h
```
