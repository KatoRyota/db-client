# Dockerによるローカル環境構築手順

## 概要

本ドキュメントはDockerを利用して、db-clientのローカル環境を構築する為の手順です。

## 前提

本ドキュメントは以下の環境における構築手順です。  
しかし、他の環境でも同様の手順で、構築できるはずです。

* Windows 10
* WSL 2 (Ubuntu 20.04 LTS)
* Docker Desktop 3

WSL 2 (Ubuntu 20.04 LTS) には、以下のソフトウェアがインストールされてる必要があります。

* Git

## sqlplusをダウンロード

以下のファイルをダウンロード。

* Basic Package (ZIP)
* SQL*Plus Package (ZIP)

```text
# [Windows]
https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html
    -> Version 19.11.0.0.0 (Requires glibc 2.14)
    -> Basic Package (ZIP)
    -> SQL*Plus Package (ZIP)
```

## OracleのDockerイメージ作成ツールをダウンロード

```shell
# [Ubuntu]
mkdir -vp ~/repo
cd ~/repo/
git clone https://github.com/oracle/docker-images
```

## db-clientをダウンロード

```shell
# [Ubuntu]
cd ~/repo/
git clone https://github.com/KatoRyota/db-client.git
```

## sqlplusの配置

前手順でダウンロードした、sqlplusのzipファイルを、  
DockerホストとDockerコンテナ間の、共有ディレクトリに配置。

```shell
# [Ubuntu]
cd `wslpath -u 'C:\Users\kator\Downloads'`

cp -vip instantclient-basic-linux.x64-19.11.0.0.0dbru.zip \
    ~/repo/db-client/docker/local/db-client/sqlplus/

cp -vip instantclient-sqlplus-linux.x64-19.11.0.0.0dbru.zip \
    ~/repo/db-client/docker/local/db-client/sqlplus/
```

## Oracle Databaseのイメージを作成

マシンスペックによりますが、Oracle DBのセットアップと起動に、30～40分程度かかります。

```shell
# [Ubuntu]
cd ~/repo/docker-images/OracleDatabase/SingleInstance/dockerfiles/
./buildContainerImage.sh -x -v 18.4.0
```

作成したOracle Databaseイメージの取り扱いには、お気を付けください。  
Docker Hubなどにアップロードすると、ライセンス違反になる可能性があります。

## Dockerコンテナの作成/起動

```shell
# [Ubuntu]
cd ~/repo/db-client/docker/local/
docker-compose up --build > stdout 2>&1 < /dev/null &
tail -f stdout
```

## 動作確認

```shell
# [Ubuntu]
docker container exec -it oracle-db-client /bin/bash

sqlplus -s 'docker/docker@//localhost:1521/XEPDB1' <<EOF
select * from employee;
EOF

exit
```

```shell
# [Ubuntu]
docker container exec -it db-client /bin/bash

export PYTHONIOENCODING=utf-8
cd /app/db-client/

python2.7 -m dbclient <<EOF | less -S
select * from employee;
EOF

python2.7 -m dbclient -t customer <<EOF | less -S
select * from customer;
EOF

exit
```

## Dockerコンテナの停止/削除

```shell
# [Ubuntu]
cd ~/repo/db-client/docker/local/
docker-compose down
```

# Tips

## Dockerコンテナを一括で作成/起動したい

```shell
# [Ubuntu]
cd ${DOCKER_COMPOSE_YML_DIR}
docker-compose up --build -d
docker-compose logs -f
```

## Dockerコンテナを一括で停止/削除したい

```shell
# [Ubuntu]
cd ${DOCKER_COMPOSE_YML_DIR}
docker-compose down
```

## Dockerリソースを一括で削除したい

```shell
# [Ubuntu]
docker container stop `docker ps -q`
docker system prune -a --volumes
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

## Dockerネットワークの一覧を確認したい

```shell
# [Ubuntu]
docker network ls
```

## Dockerボリュームの一覧を確認したい

```shell
# [Ubuntu]
docker volume ls
```

## Dockerコンテナでインタラクティブシェルを起動したい

```shell
# [Ubuntu]
docker container exec -it ${CONTAINER_NAME} /bin/bash
```

## Dockerコンテナのログを確認したい

```shell
# [Ubuntu]
docker container logs -f ${CONTAINER_NAME}
```

## Dockerコンテナの詳細を確認したい

```shell
# [Ubuntu]
docker container inspect ${CONTAINER_NAME}
```

## Dockerfileを作成したい

### for ubuntu

```shell
# [Ubuntu]
docker container run --dns=8.8.8.8 --rm \
    --name=ubuntu18-04 --hostname=ubuntu18-04 \
    -itd ubuntu:18.04

# コンテナに入って、手動で環境構築（インストールなど）を行っていき、その手順をDockerfileに記載する。
docker container exec -it ubuntu18-04 /bin/bash
```

### for centos

```shell
# [Ubuntu]
docker container run --dns=8.8.8.8 --rm \
    --name=centos7 --hostname=centos7 \
    -itd centos:7 /sbin/init
  
# コンテナに入って、手動で環境構築（インストールなど）を行っていき、その手順をDockerfileに記載する。
docker container exec -it centos7 /bin/bash
```

## Dockerfileからイメージをビルドして起動したい

```shell
# [Ubuntu]
cd ${DOCKERFILE_DIR}
docker image build -t ${IMAGE_NAME}:${VERSION} .
docker container run --dns=8.8.8.8 --rm \
    --name=${CONTAINER_NAME} --hostname=${HOST_NAME} \
    -itd ${IMAGE_NAME}:${VERSION}

docker container exec -it ${CONTAINER_NAME} /bin/bash
```

## sqlplusでOracle DBに接続したい

```shell
# [Ubuntu]
sqlplus sys/<your password>@//localhost:1521/XE as sysdba
sqlplus system/<your password>@//localhost:1521/XE
sqlplus pdbadmin/<your password>@//localhost:1521/XEPDB1
```

## Oracle Enterprise Manager Expressにアクセスしたい

```text
[Windows]
The Oracle Database inside the container also has Oracle Enterprise Manager Express configured. To access OEM Express, start your browser and follow the URL:

    https://localhost:5500/em/
```
