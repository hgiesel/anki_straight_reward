from aqt import mw, gui_hooks
from aqt.utils import showInfo, tooltip
from anki.cards import Card

from .config import get_setting

from ..utils import Answer, get_straight_len, apply_ease_change

def display_success(straightlen: int, easeplus: int):
    MSG = (
        f"Succeeded {straightlen} times in a row!<br>"
        f"Gained <b>{easeplus}</b> Ease Factor!"
    )

    tooltip(MSG)

def display_reversal(easeplus):
    MSG = (
        f"Reversed previous Ease Increase of {easeplus}!"
    )

    tooltip(MSG)

latest_info = None

def apply_strait_reward(_reviewer, card, answer: Answer):
    straightlen = get_straight_len(mw.col, card.id)

    conf = mw.col.decks.confForDid(card.did)
    sett = get_setting(mw.col, conf['name'])

    if (
        sett.straight_length >= 1 and
        straightlen >= sett.straight_length and
        (sett.start_ease * 10) < card.factor < (sett.stop_ease * 10)
    ):
        easeplus = apply_ease_change(
            card,
            sett.base_ease + (straightlen - sett.straight_length) * sett.step_ease,
        )

        global latest_info
        latest_info = (
            card.id,
            easeplus,
        )

        display_success(straightlen, easeplus)

def reverse_strait_reward(cardid: int):
    global latest_info
    card = Card(mw.col, cardid)

    if latest_info and latest_info[0] == cardid:
        apply_ease_change(card, -latest_info[1])
        display_reversal(latest_info[1])

    latest_info = None

def init_review_hook():
    gui_hooks.reviewer_did_answer_card.append(apply_strait_reward)
    gui_hooks.review_did_undo.append(reverse_strait_reward)
