from anki.cards import Card

nid = 0

for name in mw.addonManager.allAddons():
    if mw.addonManager.addonName(name) == "Straight Reward":
        am = name

cl = __import__(am).src.lib.review_hook.review_hook_closure()
cl[0]((True, 3), False, Card(mw.col, nid))
