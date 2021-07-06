import json

from aqt import mw
from pathlib import Path

from aqt.gui_hooks import deck_options_did_load
from aqt.deckoptions import DeckOptionsDialog

mw.addonManager.setWebExports(__name__, r"(web|icons)/.*\.(js|css|png)")

def init_deckoptions():
    deck_options_did_load.append(on_mount)

script_path = Path(__file__).parent / Path("../web/deckoptions.js")

with open(script_path) as file:
    script = file.read()

def on_mount(dialog):
    dialog.web.eval(script)
