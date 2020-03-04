from anki.sync import Syncer
from anki.hooks import wrap
from anki.cards import Card

from aqt import mw
from aqt.utils import showInfo, tooltip

from .config import get_setting

from ..utils import get_straight_len, apply_ease_change

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

from os.path import expanduser

def check_cardids_for_straights(self, _chunk):
    global cardids_for_straight_check

    for cid in cardids_for_straight_check:
        straightlen = get_straight_len(self.col, cid)

        did = self.col.decks.for_card_ids([cid])

        # some cards will do not have decks associated with them
        if did:
            conf = self.col.decks.confForDid(did[0])

            card = Card(self.col, cid)
            sett = get_setting(self.col, conf['name'])

            with open(expanduser('~/foobarx'), 'a+') as f:
                f.write(str(cid))
                f.write(str(conf['name']))
                f.write('\n')

            if (
                sett.straight_length >= 1 and
                straightlen >= sett.straight_length and
                (sett.start_ease * 10) < card.factor < (sett.stop_ease * 10)
            ):

                easeplus = apply_ease_change(
                    card,
                    sett.base_ease + (straightlen - sett.straight_length) * sett.step_ease,
                )

def init_sync_hook():
    Syncer.mergeRevlog = wrap(Syncer.mergeRevlog, check_mobile, pos='before')
    Syncer.applyChunk = wrap(Syncer.applyChunk, check_cardids_for_straights, pos='after')
