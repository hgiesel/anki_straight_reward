from PyQt5 import QtWidgets, Qt

from enum import IntEnum
from sys import maxsize
from itertools import takewhile
from typing import List, Tuple, Optional

version = 'v0.2'

class Answer(IntEnum):
    AGAIN = 1
    HARD = 2
    GOOD = 3
    EASY = 4

class RevlogType(IntEnum):
    LRN = 0
    REV = 1
    RELRN = 2
    EARLYREV = 3

def review_success(v: Tuple[RevlogType, Answer]) -> bool:
    return (
        v[0] in [RevlogType.REV, RevlogType.EARLYREV] and
        v[1] in [Answer.GOOD, Answer.EASY]
    )

def straight_len(lst: List[Tuple[RevlogType, Answer]]) -> int:
    straight = takewhile(review_success, lst)
    straight_length = len(list(straight))

    return straight_length

def get_straight_len(col, card_id: int):
    """Returns the length of the current straight from revlog"""

    eases = col.db.execute(
        "SELECT type, ease FROM revlog WHERE cid = ? ORDER BY id DESC",
        card_id,
    )

    return straight_len(eases.fetchall())


def force_ease_change(card, offset: int):
    card.factor += offset
    card.flushSched()

def apply_ease_change(card, reward: int, sett_min: int, sett_max: int):
    """Increase ease factor as reward for straight"""
    BARE_MINIMUM = 1300
    ABSOLUTE_MAXIMUM = 9990

    personal_maximum = sett_max * 10
    personal_minimum = sett_min * 10

    oldfactor = card.factor

    if personal_minimum <= oldfactor <= personal_maximum:
        newfactor_offset = min(
            ABSOLUTE_MAXIMUM,
            personal_maximum,
            max(
                BARE_MINIMUM,
                personal_minimum,
                card.factor + reward * 10
            )
        ) - oldfactor

        force_ease_change(card, newfactor_offset)
        return int(newfactor_offset / 10)

    return 0

def maybe_apply_reward(sett, straightlen, card) -> Optional[Tuple[int, int]]:
    if (
        sett.straight_length >= 1 and
        straightlen >= sett.straight_length
    ):
        easeplus = apply_ease_change(
            card,
            sett.base_ease + (straightlen - sett.straight_length) * sett.step_ease,
            sett.start_ease,
            sett.stop_ease,
        )

        # easeplus of 0 will react similiar to None
        return easeplus

    return None
