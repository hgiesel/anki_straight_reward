from PyQt5 import QtWidgets, Qt
from anki.cards import Card
from anki.collection import _Collection

from enum import IntEnum
from sys import maxsize
from itertools import takewhile
from typing import List, Tuple, Optional, Literal

from anki.consts import (
    BUTTON_ONE, BUTTON_TWO, BUTTON_THREE, BUTTON_FOUR,
    REVLOG_LRN, REVLOG_REV, REVLOG_RELRN, REVLOG_CRAM,
)

Button = Literal[
    BUTTON_ONE, # Again
    BUTTON_TWO, # Hard
    BUTTON_THREE, # Good
    BUTTON_FOUR, # Easy
]

RevlogType = Literal[
    REVLOG_LRN,
    REVLOG_REV,
    REVLOG_RELRN,
    REVLOG_CRAM,
]

version = 'v0.4.0'

def review_success(v: Tuple[RevlogType, Button]) -> bool:
    return (
        v[0] in [REVLOG_REV, REVLOG_CRAM] and
        v[1] in [BUTTON_THREE, BUTTON_FOUR]
    )

def straight_len(eases: List[Tuple[RevlogType, Button]]) -> int:
    straight = takewhile(review_success, eases)
    straight_length = len(list(straight))

    return straight_length

def calculate_ease_change(card: Card, reward: int, sett_min: int, sett_max: int):
    """Increase ease factor as reward for straight"""
    BARE_MINIMUM = 1300
    ABSOLUTE_MAXIMUM = 9990

    personal_maximum = sett_max * 10
    personal_minimum = sett_min * 10
    the_reward = reward * 10

    oldfactor = card.factor

    if personal_minimum <= oldfactor <= personal_maximum:
        newfactor_offset = min(
            ABSOLUTE_MAXIMUM,
            personal_maximum,
            max(
                BARE_MINIMUM,
                personal_minimum,
                card.factor + the_reward,
            )
        ) - oldfactor

        return int(newfactor_offset)

    else:
        return 0

from .config import  get_setting

# returns 250, NOT 2500
def get_easeplus(col: _Collection, card: Card, straightlen: int) -> int:
    sett = get_setting(col, card)

    if (
        sett.straight_length >= 1 and
        straightlen >= sett.straight_length
    ):
        # easeplus of 0 will be falsy
        return calculate_ease_change(
            card,
            sett.base_ease + (straightlen - sett.straight_length) * sett.step_ease,
            sett.start_ease,
            sett.stop_ease,
        )

    return 0

def get_straight_len(col: _Collection, card_id: int, skip: int = 0) -> int:
    """Returns the length of the current straight from revlog"""

    eases = col.db.execute(
        "SELECT type, ease FROM revlog WHERE cid = ? AND ivl != lastIvl ORDER BY id DESC",
        card_id,
    )

    return straight_len(eases[skip:])

def notifications_enabled(col: _Collection, card: Card) -> bool:
    return get_setting(col, card).enable_notifications
