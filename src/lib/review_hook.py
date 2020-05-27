from typing import Tuple

from aqt import mw
from aqt.gui_hooks import reviewer_will_answer_card
from aqt.utils import tooltip

from anki.hooks import card_will_flush
from anki.consts import CARD_TYPE_REV, REVLOG_REV
from anki.collection import _Collection
from anki.cards import Card

from .logic import (
    get_straight_len, get_easeplus, notifications_enabled,
    review_success, Button,
)

def display_success(straightlen: int, easeplus: int):
    MSG = (
        f"Succeeded {straightlen} times in a row.<br>"
        f"Gained <b>{easeplus}</b> Ease Factor!"
    )

    tooltip(MSG)

def card_success(card: Card, answer: Button) -> bool:
    # CARD_TYPE_* does not match to REVLOG_*, because 3 is RELRN as card type, but CRAM as revlog
    return card.type == CARD_TYPE_REV and review_success((REVLOG_REV, answer))

def from_rescheduling_deck(col: _Collection, card: Card) -> bool:
    # check whether it is a filtered deck ("dynamic") which does not reschedule
    return not col.decks.isDyn(card.did) or mw.col.decks.get(card.did)['resched']

def review_hook_closure():
    gains = {}

    def check_straight_reward(ease_tuple: Tuple[bool, int], _reviewer, card: Card) -> Tuple[bool, int]:
        nonlocal gains

        if not card_success(card, ease_tuple[1]) or not from_rescheduling_deck(mw.col, card):
            return ease_tuple

        # plus one for the current success
        straightlen = get_straight_len(mw.col, card.id) + 1
        easeplus = get_easeplus(mw.col, card, straightlen)

        if not easeplus:
            return ease_tuple

        gains[card.id] = easeplus

        if notifications_enabled(mw.col, card):
            display_success(straightlen, int(easeplus / 10))

        return ease_tuple

    def flush_with_straight_reward(card: Card):
        nonlocal gains

        if card.id not in gains:
            return

        card.factor += gains[card.id]
        del gains[card.id]

    return (
        check_straight_reward,
        flush_with_straight_reward,
    )

def init_review_hook():
    check, flush = review_hook_closure()

    reviewer_will_answer_card.append(check)
    card_will_flush.append(flush)
