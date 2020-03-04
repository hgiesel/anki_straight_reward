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

from aqt import mw

from anki.sched import Scheduler
from anki.hooks import wrap

from aqt.deckconf import DeckConf
from aqt.forms import dconf
from aqt.utils import tooltip, showInfo

from .utils import Answer, RevlogType

from .gui_conf import init_conf
from .lib.sync_hook import init_sync_hook

# Reward at every 5 strait success
STRAIGHT = 5
# Increase +15% to Ease Factor as reward
REWARD = 150
# Praise with the reward.


def review_success(v: Tuple[RevlogType, Answer]):
    return (
        v[0] in [RevlogType.REV, RevlogType.EARLYREV] and
        v[1] in [Answer.GOOD, Answer.EASY]
    )

def straight_len(lst: List[Tuple[RevlogType, Answer]]):
    straight = takewhile(review_success, lst)
    straight_length = len(list(straight))

    return straight_length

def get_straight_len(card_id: int):
    """Returns the length of the current straight from revlog"""

    eases = mw.col.db.execute(
        "SELECT type, ease FROM revlog WHERE cid = ? ORDER BY id DESC",
        card_id,
    )

    return straight_len(eases.fetchall())

def apply_reward(self, card, ease):
    """Increase ease factor as reward for straight"""
    # dconf = self.col.decks.confForDid(card.did)

    # fdfasdfasf
    # showInfo('test')
    # tooltip('bla')

    # if dconf.get('straitReward'):
    #     count = checkStraight(self, card, ease)
        # if ease == 3 and count > 0 and count % STRAIGHT == STRAIGHT - 1:
        #     card.factor = max(1300, card.factor+REWARD)
        #     tooltip(str(count+1) + PRAISE + str(card.factor/10))

from aqt import gui_hooks

def apply_strait_reward(_reviewer, card, answer: Answer):
    straight = get_straight_len(card.id)

    PRAISE = (
        f"Succeeded {straight} times in a row!<br>"
        f"Gained <b>xx</b> Ease Factor!"
    )

    from .lib.config import get_setting, write_setting
    s = get_setting('Default')
    showInfo(str(s))

    write_setting(s)

gui_hooks.reviewer_did_answer_card.append(apply_strait_reward)
init_sync_hook()
# init_review_hook()
init_conf()
