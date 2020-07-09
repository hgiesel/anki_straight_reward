from .gui import init_preferences, init_deckconf, init_addon_manager
from .lib import init_review_hook, init_sync_hook

def init():
    init_preferences()
    init_deckconf()
    init_addon_manager()
    init_review_hook()
    init_sync_hook()
