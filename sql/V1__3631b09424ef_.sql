
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 3631b09424ef

INSERT INTO alembic_version (version_num) VALUES ('3631b09424ef') RETURNING alembic_version.version_num;

