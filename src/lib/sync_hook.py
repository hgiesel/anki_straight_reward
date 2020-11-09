from typing import List, Tuple, Dict
from pathlib import Path
from datetime import datetime

from anki.collection import Collection
from anki.cards import Card
from anki.rsbackend import NotFoundError

from aqt import mw
from aqt.gui_hooks import sync_will_start, sync_did_finish
from aqt.utils import tooltip

from .logic import (
    get_straight_len,
    get_easeplus,
)

from ..utils import syncDisabled


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

def check_cid(col: Collection, card: Card, skip) -> int:
    straightlen = get_straight_len(col, card.id, skip)
    easeplus = get_easeplus(col, card, straightlen)

    card.factor += easeplus
    card.flush()

    # short factor
    return int(easeplus / 10)

def make_cid_counter(reviewed_cids: List[int]) -> Dict[int, int]:
    cid_counter = {}

    for cid in reviewed_cids:
        if cid in cid_counter:
            cid_counter[cid] += 1
        else:
            cid_counter[cid] = 0

    return cid_counter

def check_cids(col: Collection, reviewed_cids: List[int]) -> List[Tuple[int, int]]:
    result = []
    cid_counter = make_cid_counter(reviewed_cids)

    for revcid, count in cid_counter.items():
        # python ending index is always exclusive
        inclusive_count = count + 1

        # if a card was reviewed multiple times
        # we need to skip the most recent reviews for consideration
        for skip in range(inclusive_count):
            try:
                card = Card(col, revcid)
            except AssertionError:
                # card does exist in this db yet, probably created on another platform
                continue
            except NotFoundError:
                # card was reviewed remotely, but deleted locally
                continue

            # some cards do not have decks associated with them,
            # and in this case we don't know which straight settings to use, so ignore
            did = card.odid or card.did
            if not did:
                continue

            easeplus_shortened = check_cid(col, card, skip)
            result.append((revcid, easeplus_shortened))

    return result

def create_comparelog(oldids: List[int]) -> None:
    path = mw.pm.collectionPath()

    # flatten ids
    oldids.extend([
        id
        for sublist
        in mw.col.db.execute('SELECT id FROM revlog')
        for id
        in sublist
    ] if not syncDisabled.value else [])

def after_sync(oldids: List[int]) -> None:
    if len(oldids) == 0:
        return

    oldidstring = ','.join([str(oldid) for oldid in oldids])

    # exclude entries where ivl == lastIvl: they indicate a dynamic deck without rescheduling
    reviewed_cids = [
        cid
        for sublist
        in mw.col.db.execute(f'SELECT cid FROM revlog WHERE id NOT IN ({oldidstring}) and ivl != lastIvl')
        for cid
        in sublist
    ]

    result = check_cids(mw.col, reviewed_cids)

    filtered_logs = [f"cid:{r[0]} easeplus:{r[1]}" for r in result if r[1] > 0]
    filtered_length = len(filtered_logs)

    if filtered_length > 0:
        log_sync(mw.col.crt, filtered_logs)
        display_sync_info(filtered_length)

    oldids.clear()

def init_sync_hook():
    oldids = []

    sync_will_start.append(lambda: create_comparelog(oldids))
    sync_did_finish.append(lambda: after_sync(oldids))
