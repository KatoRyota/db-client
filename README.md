# db-client

本ツールは、データベースにSQLを発行して、各種操作を行う為の、コマンドラインツールです。  
内部でsqlplusやmysqlを呼び出しています。

# DEMO

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

* python >= 2.6
* sqlplus
* mysql

# Installation

TODO

# Usage

設定ファイル(`application.conf`)に、DBの接続先情報を設定して下さい。  
コンソールのエンコーディングに、utf-8を設定して下さい。  
コンソールの文字フォントに、MSゴシックなどの等幅フォントを設定して下さい。  
コンソールの環境変数[`PYTHONIOENCODING`]に、`utf-8`をセットして下さい。

以下に使い方の一例を記載します。

```shell
python -m db-client 2>&1 <<EOF | less -S
select *
from employee
;
EOF
```

指定可能なオプションは、以下のコマンドでご確認下さい。

```shell
python -m db-client -h
```