# Docker 環境構築手順
## 前提
* Windows 10
* Docker Toolbox
    
## 仮想マシンの作成
```shell script
docker-machine create \
    -d virtualbox \
    --virtualbox-disk-size 51200 \
    --virtualbox-memory 5120 \
    --virtualbox-cpu-count 2 \
    machine-1
    
docker-machine regenerate-certs machine-1
docker-machine upgrade machine-1
eval $(docker-machine env --shell bash machine-1)
```

## "Oracle Database 12c Release 2"のバイナリファイルをダウンロード。
http://www.oracle.com/technetwork/database/enterprise-edition/downloads/index.html  
-> Linux x86-64

## バイナリファイルの配置
Dockerイメージ ビルド用のディレクトリに、ダウンロードしたバイナリファイルを配置する。  
パスは環境に応じて変更すること。  

```shell script
cd 'C:\Users\kator\repo'
git clone https://github.com/oracle/docker-images

cp -vip 'C:\Users\kator\Downloads\linuxx64_12201_database.zip' \
    'C:\Users\kator\repo\docker-images\OracleDatabase\SingleInstance\dockerfiles\12.2.0.1'
```

## Docker コンテナの起動
```shell script
cd 'C:\Users\kator\repo\any-rest-api\docker'
docker-compose up --build
```
## 動作確認
```shell script
curl -s -X POST \
    -H "Content-Type: application/json" \
    -d '
        {
            "userName":"test",
            "authKey":"test",
            "payload":["ID-000-0000","ID-111-1111"]
        }
    ' \
    http://192.168.99.100:50000/getAny
```
```shell script
docker-machine ssh machine-1
docker exec -it oracle-db bash

sqlplus -s 'test/test@//localhost:1521/testPdb' <<EOF
    SELECT * FROM any_artifact;
EOF
exit
exit
```

## Docker コンテナの停止
```shell script
docker-compose down
```

# Tips
## コンテナ／ネットワーク／イメージ／ボリューム を全て作り直したい
```shell script
cd 'C:\Users\kator\repo\any-rest-api\docker'
docker-compose down
docker system prune -a --volumes
rm -vrf 'C:\Users\kator\repo\any-rest-api\docker\oracle-db\oradata'
docker-compose up --build
```
  
## 不要なリソースを削除したい
/--- 仮想マシンの削除 ---/
```shell script
docker-machine rm machine-1
```
/--- コンテナ／ネットワーク／イメージ／ボリューム の一括削除 ---/
```shell script
docker stop `docker ps -q`
docker system prune -a --volumes
```

## 仮想マシンを起動したい
```shell script
docker-machine start machine-1
eval $(docker-machine env --shell bash machine-1)
```

## 仮想マシンを再起動したい
```shell script
docker-machine restart machine-1
eval $(docker-machine env --shell bash machine-1)
```

## 仮想マシンを停止したい
```shell script
docker-machine stop machine-1
```
仮想マシンを起動したまま、Windowsのシャットダウンを行うと、 警告が表示されるが、
上記コマンドを実行し、仮想マシンを停止してから、シャットダウンを行うようにすると、 表示されなくなる。

## 仮想マシンのIPアドレスの確認したい
```shell script
docker-machine ip machine-1
```
  
## コンテナの状態を確認したい
```shell script
docker inspect any-rest-api
```
  
## "oracle-db"コンテナのサーバーにログインしたい
```shell script
docker-machine ssh machine-1
docker exec -it oracle-db bash
```
  
## sqlplus で Oracle DB に接続したい
```shell script
sqlplus / as sysdba
```
```shell script
sqlplus 'sys/!EZe8Ngz@//localhost:1521/testSid' as sysdba
```
```shell script
sqlplus 'system/!EZe8Ngz@//localhost:1521/testSid'
```
```shell script
sqlplus 'pdbadmin/!EZe8Ngz@//localhost:1521/testPdb'
```
```shell script
sqlplus -s 'test/test@//localhost:1521/testPdb'
```

## Oracle Enterprise Manager Express にアクセスしたい
```text
The Oracle Database inside the container also has Oracle Enterprise Manager Express configured. 
To access OEM Express, start your browser and follow the URL:

	https://192.168.99.100:5500/em/
```

## memo
```shell script
curl -s -X POST \
    -H "Content-Type: application/json" \
    -d '
        {
            "userName":"test",
            "authKey":"test",
            "payload":[
                {
                    "id":"ID-000-0000",
                    "name":"NAME-222-2222",
                    "type":"TYPE-222-2222"
                }
            ]
        }
    ' \
    http://192.168.99.100:50000/updateAny
```
