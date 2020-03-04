# -*- coding: utf-8 -*-
# Straight Reward:
# an Anki addon increases Ease Factor at every 5 straight success
# ("Good" or "Easy" rating in review).
# GitHub: https://github.com/luminousspice/anki-addons/
#
# Copyright: 2019 Luminous Spice <luminous.spice@gmail.com>
#            2020 Henrik Giesel <hengiesel@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

from .gui.gui_conf import init_conf
from .lib.review_hook import init_review_hook
from .lib.sync_hook import init_sync_hook

init_conf()
init_review_hook()
init_sync_hook()
