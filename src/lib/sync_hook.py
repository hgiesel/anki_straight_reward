from anki.sync import Syncer
from anki.hooks import wrap
from anki.cards import Card

from pathlib import Path
from datetime import datetime

from aqt import mw
from aqt.utils import tooltip
from aqt.addons import AddonManager

from .config import get_setting

from ..utils import get_straight_len, maybe_apply_reward

# mw is not accessible during sync
base_path = mw.addonManager._userFilesPath(__name__.split('.')[0])

def log_sync(crt, logs):
    sync_log = Path(base_path) / Path('sync_log')

    with sync_log.open('at') as f:
        f.write(f"### Ease Changes applied in collection {crt} on {datetime.now()}:\n")
        f.write('\n'.join(logs) + '\n')

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

def check_cid(col, cid):
    did = col.decks.for_card_ids([cid])

    # some cards will do not have decks associated with them
    if did:
        conf = col.decks.confForDid(did[0])

        sett = get_setting(col, conf['name'])
        straightlen = get_straight_len(col, cid)
        card = Card(col, cid)

        easeplus = maybe_apply_reward(sett, straightlen, card)

        # logging for debug purposes
        if easeplus:
            return ': '.join([str(cid), conf['name'], str(easeplus)])

    return None

def check_cardids_for_straights(self, _chunk):
    global cardids_for_straight_check

    logs = [log for log in [
        check_cid(self.col, cid)
        for cid
        in cardids_for_straight_check
    ] if log is not None]

    log_sync(self.col.crt, logs)
    cardids_for_straight_check.clear()

def init_sync_hook():
    Syncer.mergeRevlog = wrap(Syncer.mergeRevlog, check_mobile, pos='before')
    Syncer.applyChunk = wrap(Syncer.applyChunk, check_cardids_for_straights, pos='after')
