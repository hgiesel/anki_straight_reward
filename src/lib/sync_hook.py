from typing import List, Tuple
from pathlib import Path
from datetime import datetime

from anki.hooks import wrap
from anki.cards import Card
from anki.storage import Collection

from aqt import mw
from aqt.main import AnkiQt
from aqt.gui_hooks import collection_did_load
from aqt.utils import tooltip

from .config import get_setting
from ..utils import get_straight_len, get_ease_change

base_path = mw.addonManager._userFilesPath(__name__.split('.')[0])

def log_sync(crt: int, logs: List[str]) -> None:
    sync_log = Path(base_path) / Path('sync_log')

    with sync_log.open('at') as f:
        f.write(f"### Ease Changes applied in collection {crt} on {datetime.now()}:\n")
        f.write('\n'.join(logs) + '\n')

def display_sync_info(count: int):
    MSG = (
        f"Awarded Straight Reward to {count} card!"
        if count == 1
        else f"Awarded Straight Rewards to {count} cards!"
    )

    tooltip(MSG)

def check_cid(col, sett, cid) -> int:
    straightlen = get_straight_len(col, cid)
    card = Card(col, cid)

    easeplus = get_ease_change(sett, straightlen, card)
    card.factor += easeplus
    card.flush()

    return easeplus

def check_cids(col, reviewed_cids: List[int]) -> List[Tuple[int, int]]:
    result = []
    cached_setts = {}

    for revcid in reviewed_cids:
        # rev did not change interval a bit:
        # must be a filtered deck with rescheduling off
        did = col.decks.for_card_ids([revcid])

        # some cards do not have decks associated with them,
        # and in this case we don't know which straight settings to use, so ignore
        if not did:
            continue

        conf = col.decks.confForDid(did[0])

        if conf['name'] in cached_setts:
            sett = cached_setts[conf['name']]
        else:
            sett = get_setting(col, conf['name'])
            cached_setts[conf['name']] = sett

            result.append((revcid, check_cid(col, sett, revcid)))

    return result

def sync_hook_closure():
    oldids = []

    def create_comparelog(self) -> None:
        path = self.pm.collectionPath()
        col = Collection(path)

        # flatten ids
        nonlocal oldids
        oldids = [id for sublist in col.db.execute('SELECT id, ivl, lastIvl FROM revlog') for id in sublist]

    def after_sync(col) -> None:
        nonlocal oldids

        if len(oldids) == 0:
            return

        oldidstring = ','.join([str(oldid) for oldid in oldids])
        oldids.clear()

        reviewed_cids = [item for sublist in col.db.execute(f'SELECT DISTINCT cid FROM revlog WHERE id NOT IN ({oldidstring}) and ivl != lastIvl') for item in sublist]

        result = check_cids(col, reviewed_cids)

        filtered_logs = [f"cid:{r[0]} easeplus:{r[1]}" for r in result if r[1] > 0]
        filtered_length = len(filtered_logs)

        if filtered_length > 0:
            log_sync(col.crt, filtered_logs)
            display_sync_info(filtered_length)


    return {
        'create_comparelog': create_comparelog,
        'after_sync': after_sync,
    }

def init_sync_hook():
    sync_hook = sync_hook_closure()

    AnkiQt._sync = wrap(AnkiQt._sync, sync_hook['create_comparelog'], pos='before')
    collection_did_load.append(sync_hook['after_sync'])
