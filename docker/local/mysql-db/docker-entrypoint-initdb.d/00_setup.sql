CREATE DATABASE IF NOT EXISTS docker;

CREATE USER IF NOT EXISTS docker@'%' IDENTIFIED BY 'docker';
GRANT ALL ON docker.* TO docker@'%';

USE docker;

CREATE TABLE IF NOT EXISTS customer (
    id VARCHAR(300),
    name VARCHAR(300),
    type VARCHAR(300)
);

INSERT INTO customer (id, name, type)
    VALUES ('ID-000-0000', 'NAME-000-0000', 'TYPE-000-0000');
INSERT INTO customer (id, name, type)
    VALUES ('ID-111-1111', 'NAME-111-1111', 'TYPE-111-1111');
INSERT INTO customer (id, name, type)
    VALUES ('ID-222-2222', 'NAME-222-2222', 'TYPE-222-2222');
INSERT INTO customer (id, name, type)
    VALUES ('ID-333-3333', 'NAME-333-3333', 'TYPE-333-3333');
INSERT INTO customer (id, name, type)
    VALUES ('ID-444-4444', 'NAME-444-4444', 'TYPE-444-4444');
INSERT INTO customer (id, name, type)
    VALUES ('ID-555-5555', 'NAME-555-5555', 'TYPE-555-5555');
INSERT INTO customer (id, name, type)
    VALUES ('ID-666-6666', 'NAME-666-6666', 'TYPE-666-6666');
INSERT INTO customer (id, name, type)
    VALUES ('ID-777-7777', 'NAME-777-7777', 'TYPE-777-7777');
INSERT INTO customer (id, name, type)
    VALUES ('ID-888-8888', 'NAME-888-8888', 'TYPE-888-8888');
INSERT INTO customer (id, name, type)
    VALUES (CONCAT('あ\n', CHAR(13), CHAR(10), 'いうえお'),
            CONCAT('," ./\\=?!:;', CHAR(92)),
            '<<<©©©&&&');
INSERT INTO customer (id, name, type)
    VALUES ('ヲンヰヱヴーヾ・ｧｰｭｿﾏﾞﾟ',
            '¢£¬‖−〜―',
            'ソ能表');
