from anki.sync import Syncer
from anki.hooks import wrap

from aqt import mw
from aqt.utils import showInfo, tooltip

from ..main import get_straight_len
from .config import get_setting

cardids_for_straight_check = set()

def check_mobile(self, logs):
    self.col.db.execute(
        'CREATE TEMP TABLE IF NOT EXISTS comparelog AS SELECT * FROM revlog WHERE 0',
    )

    self.col.db.executemany(
        'INSERT INTO temp.comparelog VALUES (?,?,?,?,?,?,?,?,?)',
        logs,
    )

    newlogs = self.col.db.execute('SELECT * FROM temp.comparelog EXCEPT SELECT * FROM revlog')

    revset = set()

    global cardids_for_straight_check

    for mobile_rev in newlogs.fetchall():
        cardids_for_straight_check.add(mobile_rev[1])

def check_cardids_for_straights(self, _chunk):
    global cardids_for_straight_check

    for cid in cardids_for_straight_check:
        straightlen = get_straight_len(self.col, cid)

        did = self.col.decks.for_card_ids([cid])
        conf = self.col.decks.confForDid(did[0])

        tooltip(conf['name'])
        sett = get_setting(conf['name'])

        tooltip('hey')

def init_sync_hook():
    Syncer.mergeRevlog = wrap(Syncer.mergeRevlog, check_mobile, pos='before')
    Syncer.applyChunk = wrap(Syncer.applyChunk, check_cardids_for_straights, pos='after')
