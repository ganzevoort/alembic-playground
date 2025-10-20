BEGIN;

-- Running upgrade 3631b09424ef -> 4dc11366aefc

CREATE TABLE portals (
    id UUID NOT NULL, 
    name VARCHAR NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TABLE users (
    id UUID NOT NULL, 
    name VARCHAR NOT NULL, 
    portal_id UUID NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(portal_id) REFERENCES portals (id)
);

UPDATE alembic_version SET version_num='4dc11366aefc' WHERE alembic_version.version_num = '3631b09424ef';

COMMIT;

