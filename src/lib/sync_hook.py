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

def log_problem(crt, log):
    sync_log = Path(base_path) / Path('sync_log')

    with sync_log.open('at') as f:
        f.write(f"### Problem while syncing ease changes in collection {crt} on {datetime.now()}:\n")
        f.write(log + '\n')

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

    global cardids_for_straight_check

    for mobile_rev in newlogs.fetchall():
        cardids_for_straight_check.add(mobile_rev[1])

def check_cid(col, cid):
    did = col.decks.for_card_ids([cid])

    # some cards will do not have decks associated with them,
    # and in this case we don't know what reward parameters to use, so ignore
    if not did: return None

    conf = col.decks.confForDid(did[0])

    sett = get_setting(col, conf['name'])
    straightlen = get_straight_len(col, cid)
    card = Card(col, cid)

    easeplus = maybe_apply_reward(sett, straightlen, card)

    # logging for debug purposes
    if easeplus:
        return ': '.join([str(cid), conf['name'], str(easeplus)])


def check_cardids_for_straights(self):
    global cardids_for_straight_check

    try:
        logs = [log for log in [
            check_cid(self.col, cid)
            for cid
            in cardids_for_straight_check
        ] if log is not None]

        log_sync(self.col.crt, logs)

    except Exception as e:
        log_problem(self.col.crt, str(e))

    finally:
        cardids_for_straight_check.clear()

# Unused for now; use when there's a way to get the collection from a new-style hook, see:
# https://anki.tenderapp.com/discussions/add-ons/42645-getting-collection-during-new-style-sync-hook?unresolve=true
# def sync_stage_change(stage):
#     if stage == 'finalize':
#         check_cardids_for_straights()

def finish_wrapper(self, mod: int):
    check_cardids_for_straights(self)

def init_sync_hook():
    Syncer.mergeRevlog = wrap(Syncer.mergeRevlog, check_mobile, pos='before')
    # Ideally this would use hooks.sync_stage_did_change.append(sync_stage_change)
    # However, there's no way to get the collection in this case, so use a monkey patch for the self.col that Syncer has
    Syncer.finish = wrap(Syncer.finish, finish_wrapper, pos='after')
