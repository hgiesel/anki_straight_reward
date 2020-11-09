from typing import List, Tuple, Dict, Optional, Any, Callable
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

def check_cid(card: Card, skip: int) -> int:
    straightlen = get_straight_len(card.id, skip)
    easeplus = get_easeplus(card, straightlen)

    card.factor += easeplus
    card.flush()

    # short factor
    return int(easeplus / 10)

def maybe_to_card(revcid: int) -> Optional[Card]:
    try:
        return Card(mw.col, revcid)
    except AssertionError:
        # card does exist in this db yet, probably created on another platform
        return None
    except NotFoundError:
        # card was reviewed remotely, but deleted locally
        return None

def check_per_review(card: Card, count: int) -> List[int]:
    # if a card was reviewed multiple times
    # we need to skip the most recent reviews for consideration
    result = []
    for skip in range(count):

        # some cards do not have decks associated with them,
        # and in this case we don't know which straight settings to use, so ignore
        did = card.odid or card.did
        if not did:
            continue

        easeplus_shortened = check_cid(card, skip)
        result.append((card.id, easeplus_shortened))

    return result

def check(data) -> List[int]:
    revcid, count = data

    if card := maybe_to_card(revcid):
        return check_per_review(card, count)

    return []

def make_cid_counter(reviewed_cids: List[int]) -> Dict[int, int]:
    cid_counter = {}

    for cid in reviewed_cids:
        if cid in cid_counter:
            cid_counter[cid] += 1
        else:
            cid_counter[cid] = 1

    return cid_counter

def flat_map(f: Callable[[Any], List[Any]], xs: List[Any]) -> List[Any]:
    ys = []
    for x in xs:
        ys.extend(f(x))
    return ys

def check_cids(reviewed_cids: List[int]) -> List[Tuple[int, int]]:
    return flat_map(check, make_cid_counter(reviewed_cids).items())

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

    result = check_cids(reviewed_cids)

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
