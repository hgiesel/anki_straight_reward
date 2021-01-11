from aqt.preferences import Preferences
from aqt.qt import QCheckBox, QVBoxLayout

from anki.hooks import wrap

from ..utils import syncDisabled


def setup_options(pref: Preferences):
    f = pref.form

    ##### ENABLE STRAIGHT REWARD
    f.straightRewardEnabled = QCheckBox("Disable straight reward on sync")
    f.straightRewardEnabled.setChecked(syncDisabled.value)

    tabLayout = f.tab_2.findChildren(QVBoxLayout)[1]
    positionAfterForceSync = 4

    tabLayout.insertWidget(positionAfterForceSync, f.straightRewardEnabled)


def update_options(pref: Preferences):
    syncDisabled.value = pref.form.straightRewardEnabled.isChecked()


def init_preferences():
    Preferences.setupOptions = wrap(
        Preferences.setupOptions, setup_options, pos="after"
    )
    Preferences.updateOptions = wrap(
        Preferences.updateOptions, update_options, pos="before"
    )
