from .gui.gui_conf import init_conf
from .lib.review_hook import init_review_hook
from .lib.sync_hook import init_sync_hook

init_conf()
init_review_hook()
init_sync_hook()
