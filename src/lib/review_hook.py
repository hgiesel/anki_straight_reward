from aqt import mw
from aqt.gui_hooks import reviewer_will_answer_card

from aqt.utils import tooltip

from anki.hooks import card_will_flush
from anki.consts import CARD_TYPE_REV, REVLOG_REV
from anki.cards import Card
from anki.scheduler.v3 import SetSchedulingStatesRequest

from .logic import (
    get_straight_len,
    get_easeplus,
    notifications_enabled,
    review_success,
    Button,
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


def from_rescheduling_deck(card: Card) -> bool:
    # check whether it is a filtered deck ("dynamic") which does not reschedule
    return (
        not mw.col.decks.is_filtered(card.did) or mw.col.decks.get(card.did)["resched"]
    )


def check_straight_reward(
    gains: dict,
    reviewer,
    card: Card,
    rating: int,
) -> None:
    if not card_success(card, rating) or not from_rescheduling_deck(card):
        return

    # plus one for the current success
    straightlen = get_straight_len(card.id) + 1
    easeplus = get_easeplus(card, straightlen)

    if not easeplus:
        return

    if reviewer._v3:
        next_states = reviewer.get_scheduling_states()

        if rating == 3:
            next_states.good.normal.review.ease_factor += easeplus / 1000
        else:
            next_states.easy.normal.review.ease_factor += easeplus / 1000

        request = SetSchedulingStatesRequest(
            key=reviewer._state_mutation_key,
            states=next_states,
        )
        reviewer.set_scheduling_states(request)
    else:
        gains[card.id] = easeplus

    if notifications_enabled(card):
        display_success(straightlen, int(easeplus / 10))


def on_will_answer_card(
    gains: dict,
    ease_tuple: tuple[bool, int],
    reviewer,
    card: Card,
) -> tuple[bool, int]:
    check_straight_reward(gains, reviewer, card, ease_tuple[1])
    return ease_tuple


def flush_with_straight_reward(gains: dict, card: Card) -> None:
    if card.id not in gains:
        return

    card.factor += gains[card.id]
    del gains[card.id]


def init_review_hook():
    gains = {}

    reviewer_will_answer_card.append(
        lambda ease_tuple, reviewer, card: on_will_answer_card(
            gains, ease_tuple, reviewer, card
        ),
    )

    card_will_flush.append(
        lambda card: flush_with_straight_reward(gains, card),
    )
