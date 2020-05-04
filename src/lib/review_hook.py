from typing import Tuple

from aqt import mw, gui_hooks
from anki import hooks

from aqt.utils import tooltip
from anki.cards import Card

from .config import get_setting

from ..utils import (
    BUTTON_THREE, BUTTON_FOUR,
    get_straight_len, get_ease_change,
)

def display_success(straightlen: int, easeplus: int):
    MSG = (
        f"Succeeded {straightlen} times in a row.<br>"
        f"Gained <b>{easeplus}</b> Ease Factor!"
    )

    tooltip(MSG)

def review_hook_closure():
    gains = {}

    def check_straight_reward(ease_tuple: Tuple[bool, int], _reviewer, card) -> Tuple[bool, int]:
        nonlocal gains

        if ease_tuple[1] not in [BUTTON_THREE, BUTTON_FOUR]:
            return ease_tuple

        # plus One for the current success
        straightlen = get_straight_len(mw.col, card.id) + 1

        # check whether it is a filtered deck ("dynamic") which does not reschedule
        if mw.col.decks.isDyn(card.did) and not mw.col.decks.get(card.did)['resched']:
            return ease_tuple

        conf = mw.col.decks.confForDid(card.odid or card.did)
        sett = get_setting(mw.col, conf['name'])

        easeplus = get_ease_change(sett, straightlen, card)

        if not easeplus:
            return ease_tuple

        gains[card.id] = easeplus

        if sett.enable_notifications:
            display_success(straightlen, int(easeplus / 10))

        return ease_tuple

    def flush_with_straight_reward(card):
        nonlocal gains

        if card.id not in gains:
            return

        card.factor += gains[card.id]
        del gains[card.id]

    return {
        'check': check_straight_reward,
        'flush': flush_with_straight_reward,
    }

def init_review_hook():
    review_hook = review_hook_closure()

    gui_hooks.reviewer_will_answer_card.append(review_hook['check'])
    hooks.card_will_flush.append(review_hook['flush'])
