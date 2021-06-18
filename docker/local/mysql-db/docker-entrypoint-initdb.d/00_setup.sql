CREATE DATABASE IF NOT EXISTS docker;

CREATE USER IF NOT EXISTS docker@'%' IDENTIFIED BY 'docker';
GRANT ALL ON docker.* TO docker@'%';

USE docker;

CREATE TABLE IF NOT EXISTS employee (
    id VARCHAR(20),
    name VARCHAR(20),
    type VARCHAR(20)
);

INSERT INTO employee (id, name, type)
    VALUES ('ID-000-0000', 'NAME-000-0000', 'TYPE-000-0000');
INSERT INTO employee (id, name, type)
    VALUES ('ID-111-1111', 'NAME-111-1111', 'TYPE-111-1111');