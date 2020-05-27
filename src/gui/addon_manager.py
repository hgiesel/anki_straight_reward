from aqt import mw
from aqt.utils import showInfo

def show_info():
    showInfo(
        'The configuration via meta.json is phased out since Straight Reward v0.4.\n\n'
        'To configure the functionality of this add-on, go to the Deck Overview, '
        'choose a Deck, click the wheel to its right, select "Options", and in the resulting window '
        'open the "Rewards" tab.'
    )

def init_addon_manager():
    mw.addonManager.setConfigAction(__name__, show_info)
