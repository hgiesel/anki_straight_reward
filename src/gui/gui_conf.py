from PyQt5 import QtWidgets, Qt, QtCore

from aqt import mw
from aqt.deckconf import DeckConf
from aqt.forms import dconf

from anki.hooks import wrap

from ..lib.config_types import StraightSetting
from ..lib.config import (
    get_setting, get_default_setting,
    write_setting,
    remove_setting, rename_setting,
)

def setup_reward_tab(self, Dialog):
    """Add an option tab for Straight Reward at Review section on Deckconf dialog."""
    w = QtWidgets.QWidget()
    self.gridLayout_straight = QtWidgets.QGridLayout()
    self.gridLayout_straight.setColumnStretch(1, 5)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

    ##### STRAIGHT LENGTH
    self.straightLengthLabel = QtWidgets.QLabel(w)
    self.straightLengthLabel.setText(_('Begin at straight of length'))
    self.gridLayout_straight.addWidget(self.straightLengthLabel, 1, 0, 1, 1)

    self.straightLengthSpinBox = QtWidgets.QSpinBox(w)
    self.straightLengthSpinBox.setMinimum(0)
    self.straightLengthSpinBox.setMaximum(100)
    self.gridLayout_straight.addWidget(self.straightLengthSpinBox, 1, 1, 1, 2)

    ##### ENABLE NOTIFICATIONS
    self.straightEnableNotificationsLabel = QtWidgets.QLabel(w)
    self.straightEnableNotificationsLabel.setText(_('Enable notifications'))
    self.gridLayout_straight.addWidget(self.straightEnableNotificationsLabel, 2, 0, 1, 1)

    self.straightEnableNotificationsCheckBox = QtWidgets.QCheckBox(w)
    self.gridLayout_straight.addWidget(self.straightEnableNotificationsCheckBox, 2, 1, 1, 2)

    ##### BASE EASE
    self.straightBaseEaseLabel = QtWidgets.QLabel(w)
    self.straightBaseEaseLabel.setText(_('Base ease reward'))
    self.gridLayout_straight.addWidget(self.straightBaseEaseLabel, 3, 0, 1, 1)

    self.straightBaseEaseSpinBox = QtWidgets.QSpinBox(w)
    self.straightBaseEaseSpinBox.setSuffix('%')
    self.straightBaseEaseSpinBox.setMinimum(0)
    self.straightBaseEaseSpinBox.setMaximum(999)
    self.gridLayout_straight.addWidget(self.straightBaseEaseSpinBox, 3, 1, 1, 2)

    ##### STEP EASE
    self.straightStepEaseLabel = QtWidgets.QLabel(w)
    self.straightStepEaseLabel.setText(_('Step ease reward'))
    self.gridLayout_straight.addWidget(self.straightStepEaseLabel, 4, 0, 1, 1)

    self.straightStepEaseSpinBox = QtWidgets.QSpinBox(w)
    self.straightStepEaseSpinBox.setSuffix('%')
    self.straightStepEaseSpinBox.setMinimum(0)
    self.straightStepEaseSpinBox.setMaximum(999)
    self.gridLayout_straight.addWidget(self.straightStepEaseSpinBox, 4, 1, 1, 2)

    ##### START EASE
    self.straightStartEaseLabel = QtWidgets.QLabel(w)
    self.straightStartEaseLabel.setText(_('Start at ease'))
    self.gridLayout_straight.addWidget(self.straightStartEaseLabel, 5, 0, 1, 1)

    self.straightStartEaseSpinBox = QtWidgets.QSpinBox(w)
    self.straightStartEaseSpinBox.setSuffix('%')
    self.straightStartEaseSpinBox.setMinimum(130)
    self.straightStartEaseSpinBox.setMaximum(999)
    self.gridLayout_straight.addWidget(self.straightStartEaseSpinBox, 5, 1, 1, 2)

    ##### STOP EASE
    self.straightStopEaseLabel = QtWidgets.QLabel(w)
    self.straightStopEaseLabel.setText(_('Stop at ease'))
    self.gridLayout_straight.addWidget(self.straightStopEaseLabel, 6, 0, 1, 1)

    self.straightStopEaseSpinBox = QtWidgets.QSpinBox(w)
    self.straightStopEaseSpinBox.setSuffix('%')
    self.straightStopEaseSpinBox.setMinimum(130)
    self.straightStopEaseSpinBox.setMaximum(999)
    self.gridLayout_straight.addWidget(self.straightStopEaseSpinBox, 6, 1, 1, 2)

    ##### VERTICAL SPACER
    verticalSpacer = QtWidgets.QSpacerItem(20, 150, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    self.gridLayout_straight.addItem(verticalSpacer)

    w.setLayout(self.gridLayout_straight)
    self.tabWidget.insertTab(2, w, 'Straight Rewards')

def load_reward_tab(self):
    """Get the option for Straight Reward."""
    straight_conf = get_setting(mw.col, self.conf['name'])

    f = self.form
    f.straightLengthSpinBox.setValue(straight_conf.straight_length)
    f.straightEnableNotificationsCheckBox.setChecked(straight_conf.enable_notifications)
    f.straightBaseEaseSpinBox.setValue(straight_conf.base_ease)
    f.straightStepEaseSpinBox.setValue(straight_conf.step_ease)
    f.straightStartEaseSpinBox.setValue(straight_conf.start_ease)
    f.straightStopEaseSpinBox.setValue(straight_conf.stop_ease)

def save_reward_tab(self):
    """Save the option for Straight Reward."""
    f = self.form

    result = StraightSetting(
        self.conf['name'],
        f.straightLengthSpinBox.value(),
        f.straightEnableNotificationsCheckBox.isChecked(),
        f.straightBaseEaseSpinBox.value(),
        f.straightStepEaseSpinBox.value(),
        f.straightStartEaseSpinBox.value(),
        f.straightStopEaseSpinBox.value(),
    )

    write_setting(mw.col, result)

def restore_reward_tab(self):
    straight_conf = get_default_setting(self.conf['name'])

    f = self.form
    f.straightLengthSpinBox.setValue(straight_conf.straight_length)
    f.straightBaseEaseSpinBox.setValue(straight_conf.base_ease)
    f.straightStepEaseSpinBox.setValue(straight_conf.step_ease)
    f.straightStartEaseSpinBox.setValue(straight_conf.start_ease)
    f.straightStopEaseSpinBox.setValue(straight_conf.stop_ease)

def remove_straight_setting(self, _old):
    save_names = {c['name'] for c in mw.col.decks.allConf()}

    _old(self)

    new_names = {c['name'] for c in mw.col.decks.allConf()}

    name_for_deletion = save_names.difference(new_names)

    if len(name_for_deletion) == 1:
        remove_setting(mw.col, name_for_deletion.pop())

    # otherwise user renamed conf to old name, or reuses name 

# unused
def rename_straight_setting(self, _old):
    save_names = {c['name'] for c in mw.col.decks.allConf()}

    _old(self)

    new_names = {c['name'] for c in mw.col.decks.allConf()}

    old_name = save_names.difference(new_names)
    new_name = new_names.difference(save_names)

    if len(old_name) == 1 and len(new_name) == 1:
        rename_setting(
            mw.col,
            old_name.pop(),
            new_name.pop(),
        )

    # otherwise user renamed conf to old name, or reuses name 

def init_conf():
    dconf.Ui_Dialog.setupUi = wrap(dconf.Ui_Dialog.setupUi, setup_reward_tab)

    DeckConf.onRestore = wrap(DeckConf.onRestore, restore_reward_tab)
    DeckConf.loadConf = wrap(DeckConf.loadConf, load_reward_tab)
    DeckConf.saveConf = wrap(DeckConf.saveConf, save_reward_tab, 'before')

    DeckConf.remGroup = wrap(DeckConf.remGroup, remove_straight_setting, 'around')
    DeckConf.renameGroup = wrap(DeckConf.renameGroup, remove_straight_setting, 'around')

    # gui_hooks.deck_conf_did_setup_ui_form.append(setup_reward_tab)
    # gui_hooks.deck_conf_did_load_config.append(load_reward_tab)
    # gui_hooks.deck_conf_will_save_config.append(save_reward_tab)
