import os
import copy

from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.command import upgrade


class MyConfig(Config):
    def __init__(self, **kwargs):
        super().__init__(file_="alembic.ini", **kwargs)


def make_sql(sql_file, revision):
    if os.path.exists(sql_file):
        return
    with open(sql_file, "w") as buffer:
        from_to = f"{revision.down_revision or 'base'}:{revision.revision}"
        config = MyConfig(output_buffer=buffer)
        upgrade(config, from_to, sql=True)


def all_revisions():
    script = ScriptDirectory.from_config(MyConfig())
    return reversed(list(script.walk_revisions()))


if __name__ == "__main__":
    os.makedirs("sql", exist_ok=True)
    for index, revision in enumerate(all_revisions(), start=1):
        sql_file = f"sql/V{index}__{revision.module.__name__}"
        make_sql(sql_file, revision)
