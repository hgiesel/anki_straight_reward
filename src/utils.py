from PyQt5 import QtWidgets, Qt

from enum import IntEnum
from sys import maxsize
from itertools import takewhile
from typing import List, Tuple

version = "v0.1"

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

def review_success(v: Tuple[RevlogType, Answer]):
    return (
        v[0] in [RevlogType.REV, RevlogType.EARLYREV] and
        v[1] in [Answer.GOOD, Answer.EASY]
    )

def straight_len(lst: List[Tuple[RevlogType, Answer]]):
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

def apply_ease_change(card, reward: int):
    """Increase ease factor as reward for straight"""
    oldfactor = card.factor
    card.factor = min(9990, max(1300, card.factor + reward * 10))

    card.flushSched()

    return int((card.factor - oldfactor)/10)
