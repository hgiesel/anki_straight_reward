# -*- coding: utf-8 -*-
# Straight Reward:
# an Anki addon increases Ease Factor at every 5 straight success
# ("Good" or "Easy" rating in review).
# GitHub: https://github.com/luminousspice/anki-addons/
#
# Copyright: 2019 Luminous Spice <luminous.spice@gmail.com>
#            2020 Henrik Giesel <hengiesel@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

from PyQt5 import QtWidgets, Qt

from sys import maxsize
from itertools import takewhile
from typing import List, Tuple

from .utils import Answer, RevlogType

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

from .gui.gui_conf import init_conf
from .lib.review_hook import init_review_hook
from .lib.sync_hook import init_sync_hook

init_sync_hook()
init_review_hook()
init_conf()
