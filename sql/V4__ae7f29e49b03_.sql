
-- Running upgrade 4dc11366aefc -> ae7f29e49b03

ALTER TABLE portals ADD COLUMN logo VARCHAR;

UPDATE alembic_version SET version_num='ae7f29e49b03' WHERE alembic_version.version_num = '4dc11366aefc';

