from anki.sync import Syncer
from anki.hooks import wrap

from aqt.utils import showInfo
from os.path import expanduser

def foo(self, logs):

    self.col.db.execute(
        'CREATE TEMP TABLE IF NOT EXISTS comparelog AS SELECT * FROM revlog WHERE 0',
    )

    self.col.db.executemany(
        'INSERT INTO temp.comparelog VALUES (?,?,?,?,?,?,?,?,?)',
        logs,
    )

    newlogs = self.col.db.execute('SELECT * FROM temp.comparelog EXCEPT SELECT * FROM revlog')

    with open(expanduser('~/myfilex'), 'w+') as f:
        f.write('Foo bla bla\n')
        f.write(str(newlogs.fetchall()))

def init_sync_hook():
    Syncer.mergeRevlog = wrap(Syncer.mergeRevlog, foo, pos='before')
