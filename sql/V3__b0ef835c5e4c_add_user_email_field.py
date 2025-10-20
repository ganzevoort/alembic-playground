BEGIN;

-- Running upgrade 4dc11366aefc -> b0ef835c5e4c

ALTER TABLE users ADD COLUMN email VARCHAR;

UPDATE alembic_version SET version_num='b0ef835c5e4c' WHERE alembic_version.version_num = '4dc11366aefc';

COMMIT;

