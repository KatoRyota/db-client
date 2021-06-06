# Dockerによるローカル環境構築手順

## 概要

本ドキュメントはDockerを利用して、db-clientのローカル環境を構築する為の手順です。

## 前提

本ドキュメントは以下の環境における構築手順です。  
しかし、他の環境でも同様の手順で構築できるはずです。

* Windows 10
* WSL 2 (Ubuntu 20.04 LTS)
* Docker Desktop 3

WSL 2 (Ubuntu 20.04 LTS)上には、以下のソフトウェアがインストールされてる必要があります。

* Git

## Oracle Database 12c Release 2をダウンロード

```text
# [Windows]
http://www.oracle.com/technetwork/database/enterprise-edition/downloads/index.html  
    -> Linux x86-64  
```

## Dockerイメージをビルドする為の、関連ファイルをダウンロード

```shell
# [Ubuntu]
cd ~/repo
git clone https://github.com/oracle/docker-images
```

## バイナリファイルの配置

前手順でダウンロードした、Oracle Database 12c Release 2のバイナリファイルを、  
Dockerイメージのビルド用ディレクトリに配置。  
パスは環境に応じて変更すること。

```shell
# [Ubuntu]
cd `wslpath -u 'C:\Users\kator\Downloads'`
cp -vip linuxx64_12201_database.zip \
    ~/repo/docker-images/OracleDatabase/SingleInstance/dockerfiles/12.2.0.1
```

## db-clientをダウンロード

```shell
# [Ubuntu]
cd ~/repo
git clone https://github.com/KatoRyota/db-client.git
```

## Docker上のリソースを全て削除

```shell
# [Ubuntu]
docker stop `docker ps -q`
docker system prune -a --volumes
```

## Dockerコンテナの起動

```shell
# [Ubuntu]
cd ~/repo/db-client/docker/local
docker-compose up --build > stdout 2>&1 < /dev/null &
tail -f stdout
```

## 動作確認

```shell
# [Ubuntu]
docker container exec -it oracle-db bash

sqlplus -s 'test/test@//localhost:1521/testPdb' <<EOF
SELECT * FROM any_artifact;
EOF

exit
```

## Dockerコンテナの停止

```shell
# [Ubuntu]
cd ~/repo/db-client/docker/local
docker-compose down
```

# Tips

## Dockerコンテナを一括起動したい

```shell
# [Ubuntu]
cd ${APP_ROOT_DIR}
docker-compose up --build > stdout 2>&1 < /dev/null &
```

## Dockerコンテナを一括停止したい

```shell
# [Ubuntu]
cd ${APP_ROOT_DIR}
docker-compose down
```

## Docker上のリソースを一括削除したい

```shell
# [Ubuntu]
docker stop `docker ps -q`
docker system prune -a --volumes
```

## Dockerコンテナにログインしたい

```shell
# [Ubuntu]
docker container exec -it ${CONTAINER_NAME} bash
```

## Dockerコンテナの一覧を確認したい

```shell
# [Ubuntu]
docker container ls -a
```

## Dockerイメージの一覧を確認したい

```shell
# [Ubuntu]
docker image ls -a
```

## Dockerコンテナの状態を確認したい

```shell
# [Ubuntu]
docker container inspect ${CONTAINER_NAME}
```

## sqlplusでOracle DBに接続したい

```shell
# [Ubuntu]
#1
sqlplus / as sysdba
#2
sqlplus 'sys/!EZe8Ngz@//localhost:1521/testSid' as sysdba
#3
sqlplus 'system/!EZe8Ngz@//localhost:1521/testSid'
#4
sqlplus 'pdbadmin/!EZe8Ngz@//localhost:1521/testPdb'
#5
sqlplus -s 'test/test@//localhost:1521/testPdb'
```

## Oracle Enterprise Manager Expressにアクセスしたい

```text
[Windows]
The Oracle Database inside the container also has Oracle Enterprise Manager Express configured. 
To access OEM Express, start your browser and follow the URL:

	https://192.168.99.100:5500/em/
```
