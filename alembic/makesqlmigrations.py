import sys
import os
import re
import copy
from glob import glob

from alembic.config import Config as AlembicConfig
from alembic.script import ScriptDirectory
from alembic.command import upgrade
from alembic.util import rev_id


class AlembicCommandWrapper():
    config_kwargs = {"file_": "alembic.ini"}

    def __init__(self):
        self.config = AlembicConfig(**self.config_kwargs)
        self.script = ScriptDirectory.from_config(self.config)

    def all_revisions(self):
        return reversed(list(self.script.walk_revisions()))

    def heads(self):
        return self.script.get_revisions(self.script.get_heads())

    def merge_heads(self):
        heads = self.script.get_heads()
        self.script.generate_revision(rev_id=rev_id(), head=heads)

    def upgrade(self, *args):
        upgrade(self.config, *args)

    def write_sql(self, buffer, revision):
        from_to = f"{revision.down_revision or 'base'}:{revision.revision}"
        config = AlembicConfig(output_buffer=buffer, **self.config_kwargs)
        upgrade(config, from_to, sql=True)


MERGE_SQL_STATEMENT = """
    BEGIN;

    UPDATE alembic_version
    SET version_num='{revision}'
    WHERE alembic_version.version_num in {down_revisions};

    COMMIT;
"""


class FlyWayRevisionConflict(Exception):
    """
    We have a revision with multiple SQL files.
    This shouldn't happen.
    """


class FlyWayBranchConflict(Exception):
    """
    We have multiple SQL files ("V{version}__{comment}.sql").
    This probably happened because they were created in separate
    branches. The ones that were in the master branch have been
    deployed to staging and possibly production too, so they *should*
    be kept.
    The best way forward is to remove any SQL file that were not
    in master, this script can recreate them.
    """


class SQLDirectory:
    def __init__(self, alembic, directory="sql"):
        self.directory = directory
        self.revisions = set()
        self.sequence = set()
        os.makedirs(self.directory, exist_ok=True)
        for filename in glob("V*.sql", root_dir=self.directory):
            if match := re.match(r"V(\d+)__([\da-f]{12})_(.*)\.sql$", filename):
                sequence_nr, revision_id, comment = match.groups()
                if revision_id in self.revisions:
                    raise FlyWayRevisionConflict(f"{revision_id} not unique")
                self.revisions.add(revision_id)
            elif match := re.match(r"V(\d+)__(.*)\.sql$", filename):
                sequence_nr, comment = match.groups()
            if int(sequence_nr) in self.sequence:
                raise FlyWayBranchConflict(f"V{sequence_nr} not unique")
            self.sequence.add(int(sequence_nr))

    def merge_sql_command(self, revision):
        return MERGE_SQL_STATEMENT.format(
            revision=revision.revision, 
            down_revisions=str(revision.down_revision),
        )

    def make_sql(self, revision):
        if revision.revision in self.revisions:
            return
        base = re.sub(r"_py$", "", revision.module.__name__)
        sequence_nr = max(self.sequence, default=0) + 1
        self.sequence.add(sequence_nr)
        sql_file = f"{self.directory}/V{sequence_nr}__{base}.sql"
        print(f"Create {sql_file}")
        with open(sql_file, "w") as buffer:
            if isinstance(revision.down_revision, tuple):
                # It's a merge. Both branches have their sql already
                # emitted. Now correct the alembic_version.
                buffer.write(self.merge_sql_command(revision))
            else:
                alembic.write_sql(buffer, revision)


if __name__ == "__main__":
    alembic = AlembicCommandWrapper()
    alembic.upgrade("heads")
    if len(alembic.heads()) > 1:
        alembic.merge_heads()
        alembic.upgrade("heads")

    try:
        sqldir = SQLDirectory(alembic)
    except (FlyWayRevisionConflict, FlyWayBranchConflict) as e:
        print(f"\n{e}")
        print(e.__doc__)
        sys.exit(4)
    for revision in alembic.all_revisions():
        sqldir.make_sql(revision)
