# Dockerによるローカル環境構築手順

## 概要

本ドキュメントはDockerを利用して、experimental-toolsのローカル環境を構築する為の手順です。  
依存アプリケーションは、固定データを返すテスト用アプリケーションです。

## 前提

本ドキュメントは以下の環境における構築手順です。  
ただ、他の環境でも、同様の手順で構築できるはずです。

* Windows 10
* WSL 2 (Ubuntu 20.04 LTS)
* Docker Desktop 3
* JDK 11
* Maven 3

## アプリケーションのビルド

```shell
# [Windows]
mvn clean package -Dmaven.test.skip=true
```

## Docker上のリソースを全て削除

```shell
# [Ubuntu]
docker stop `docker ps -q`
docker system prune -a --volumes
```

## アプリケーションを削除

```shell
# [Ubuntu]
cd ~/app/
rm -vrf ./distribution-0.0.1-SNAPSHOT*
```

## アプリケーションの配置

```shell
# [Ubuntu]
cp -vip `wslpath -u 'C:\Users\kator\IdeaProjects\experimental-tools\distribution\target\distribution-0.0.1-SNAPSHOT-local-bin.tar.gz'` ~/app/

cd ~/app/
tar xzvf distribution-0.0.1-SNAPSHOT-local-bin.tar.gz
```

## Dockerコンテナの起動

```shell script
# [Ubuntu]
cd ~/app/distribution-0.0.1-SNAPSHOT/
docker-compose up --build > stdout 2>&1 < /dev/null &
tail -f stdout
```

## 動作確認

```shell
# [Ubuntu]
curl -s -X GET  "http://localhost:50001/employees"
curl -s -X GET  "http://localhost:50002/getLatestMessages?requestId=000-000-000&threadId=10&latestMessageId=20"

cd ~/app/distribution-0.0.1-SNAPSHOT/employees-api/log/
tail -f application.log
tail -f access.log
```

## Dockerコンテナの停止

```shell
# [Ubuntu]
cd ~/app/distribution-0.0.1-SNAPSHOT/
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
docker container exec -it ${CONTAINER_NAME} /bin/bash
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
