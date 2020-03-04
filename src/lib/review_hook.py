from aqt import mw, gui_hooks
from aqt.utils import tooltip
from anki.cards import Card

from .config import get_setting

from ..utils import Answer, get_straight_len, maybe_apply_reward, apply_ease_change

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

latest_info = {}

def check_for_straight_reward(_reviewer, card, answer: Answer):
    straightlen = get_straight_len(mw.col, card.id)

    conf = mw.col.decks.confForDid(card.did)
    sett = get_setting(mw.col, conf['name'])

    easeplus = maybe_apply_reward(sett, straightlen, card)

    if easeplus:
        latest_info[card.id] = easeplus
        display_success(straightlen, easeplus)

    elif card.id in latest_info:
        del latest_info[card.id]

def reverse_strait_reward(cardid: int):
    global latest_info
    card = Card(mw.col, cardid)

    if cardid in latest_info:
        apply_ease_change(card, -latest_info[cardid])
        display_reversal(latest_info[cardid])

        del latest_info[cardid]

def init_review_hook():
    gui_hooks.reviewer_did_answer_card.append(check_for_straight_reward)
    gui_hooks.review_did_undo.append(reverse_strait_reward)
