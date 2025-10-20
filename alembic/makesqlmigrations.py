import os
import re
import copy
from glob import glob

from alembic.config import Config as AlembicConfig
from alembic.script import ScriptDirectory
from alembic.command import upgrade


class Config(AlembicConfig):
    def __init__(self, **kwargs):
        super().__init__(file_="alembic.ini", **kwargs)


def all_revisions():
    script = ScriptDirectory.from_config(Config())
    return reversed(list(script.walk_revisions()))


class SQLDirectory:
    def __init__(self, directory="sql"):
        self.directory = directory
        self.revisions = set()
        self.sequence = set()
        os.makedirs(self.directory, exist_ok=True)
        for filename in glob("V*.py", root_dir=self.directory):
            if match := re.match(r"V(\d+)__([\da-f]{12})_(.*)\.py$", filename):
                sequence_nr, revision_id, comment = match.groups()
                if revision_id in self.revisions:
                    raise Exception(f"{revision_id} not unique")
                self.revisions.add(revision_id)
            elif match := re.match(r"V(\d+)__(.*)\.py$", filename):
                sequence_nr, comment = match.groups()
            if sequence_nr in self.sequence:
                raise Exception(f"V{sequence_nr} not unique")
            self.sequence.add(sequence_nr)

    def make_sql(self, revision):
        if revision.revision in self.revisions:
            return
        base = re.sub(r"_py$", "", revision.module.__name__)
        sequence_nr = max(self.sequence, default=0) + 1
        self.sequence.add(sequence_nr)
        sql_file = f"{self.directory}/V{sequence_nr}__{base}.py"
        with open(sql_file, "w") as buffer:
            from_to = f"{revision.down_revision or 'base'}:{revision.revision}"
            config = Config(output_buffer=buffer)
            upgrade(config, from_to, sql=True)


if __name__ == "__main__":
    sqldir = SQLDirectory()
    for revision in all_revisions():
        sqldir.make_sql(revision)
