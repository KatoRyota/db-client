ALTER SESSION SET CONTAINER = XEPDB1;

CREATE USER docker
    IDENTIFIED BY "docker"
    DEFAULT TABLESPACE USERS
    TEMPORARY TABLESPACE TEMP
    QUOTA UNLIMITED ON USERS;

GRANT CONNECT, RESOURCE TO docker;

CONNECT docker/docker@//localhost:1521/XEPDB1;

CREATE TABLE employee (
    id VARCHAR2(300),
    name VARCHAR2(300),
    type VARCHAR2(300)
);

INSERT INTO employee (id, name, type)
    VALUES ('ID-000-0000', 'NAME-000-0000', 'TYPE-000-0000');
INSERT INTO employee (id, name, type)
    VALUES ('ID-111-1111', 'NAME-111-1111', 'TYPE-111-1111');
INSERT INTO employee (id, name, type)
    VALUES ('ID-222-2222', 'NAME-222-2222', 'TYPE-222-2222');
INSERT INTO employee (id, name, type)
    VALUES ('ID-333-3333', 'NAME-333-3333', 'TYPE-333-3333');
INSERT INTO employee (id, name, type)
    VALUES ('ID-444-4444', 'NAME-444-4444', 'TYPE-444-4444');
INSERT INTO employee (id, name, type)
    VALUES ('ID-555-5555', 'NAME-555-5555', 'TYPE-555-5555');
INSERT INTO employee (id, name, type)
    VALUES ('ID-666-6666', 'NAME-666-6666', 'TYPE-666-6666');
INSERT INTO employee (id, name, type)
    VALUES ('ID-777-7777', 'NAME-777-7777', 'TYPE-777-7777');
INSERT INTO employee (id, name, type)
    VALUES ('ID-888-8888', 'NAME-888-8888', 'TYPE-888-8888');
INSERT INTO employee (id, name, type)
    VALUES ('ID-999-9999', 'NAME-999-9999', 'TYPE-999-9999');
INSERT INTO employee (id, name, type)
    VALUES ('あ\n' || CHR(13) || CHR(10) || 'いうえお',
            '," ./\\=?!:;' || CHR(92),
            '<<<©©©&&&');

COMMIT;
exit;
