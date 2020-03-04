# -*- coding: utf-8 -*-
# Straight Reward:
# an Anki addon increases Ease Factor at straight success
# ("Good" or "Easy" rating in review).
# GitHub: https://github.com/luminousspice/anki-addons/
#         https://github.com/hgiesel/anki_straight_reward/
#
# Copyright: 2019 Luminous Spice <luminous.spice@gmail.com>
#            2020 Henrik Giesel <hengiesel@gmail.com>
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

from aqt import mw
import os.path as path

if mw.addonManager.addonName(path.dirname(__file__)) != 'Straight Reward':
    dir_path = path.dirname(path.realpath(__file__))

    with open(path.join(dir_path, 'manifest.json')) as f:
        if path.exists('meta.json'):
            with open(path.join(dir_path, 'meta.json')) as f_old:
                import json
                mw.addonManager.writeAddonMeta(dir_path, json.load(f).update({
                    'config': json.load(f_old)['config']
                }))

from .src import main
