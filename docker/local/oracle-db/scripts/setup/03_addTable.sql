CONNECT test/test@//localhost:1521/testPdb;

CREATE TABLE employee (
    id VARCHAR2(20),
    name VARCHAR2(20),
    type VARCHAR2(20)
);

INSERT INTO any_artifact (id, name, type)
    VALUES ('ID-000-0000', 'NAME-000-0000', 'TYPE-000-0000');
INSERT INTO any_artifact (id, name, type)
    VALUES ('ID-111-1111', 'NAME-111-1111', 'TYPE-111-1111');

COMMIT;
exit;
