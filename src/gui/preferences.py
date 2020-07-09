from PyQt5 import QtWidgets

from aqt.preferences import Preferences

from anki.hooks import wrap

from ..utils import syncDisabledKeyword

def setup_options(pref: Preferences):
    f = pref.form

    ##### ENABLE STRAIGHT REWARD
    f.straightRewardEnabled = QtWidgets.QCheckBox('Disable straight reward on sync')
    f.straightRewardEnabled.setChecked(pref.prof.get(syncDisabledKeyword, False))

    tabLayout = f.tab_2.findChildren(QtWidgets.QVBoxLayout)[1]
    positionAfterForceSync = 4

    tabLayout.insertWidget(positionAfterForceSync, f.straightRewardEnabled)

def update_options(pref: Preferences):
    pref.prof[syncDisabledKeyword] = pref.form.straightRewardEnabled.isChecked()

def init_preferences():
    Preferences.setupOptions = wrap(Preferences.setupOptions, setup_options, pos='after')
    Preferences.updateOptions = wrap(Preferences.updateOptions, update_options, pos='before')
