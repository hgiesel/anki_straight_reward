from PyQt5 import QtWidgets, Qt

from aqt.deckconf import DeckConf
from aqt.forms import dconf

from anki.hooks import wrap

def setup_reward_tab(self, Dialog):
    """Add an option tab for Straight Reward at Review section on Deckconf dialog."""
    w = QtWidgets.QWidget()
    self.gridLayout_straight = QtWidgets.QGridLayout()

    ##### STRAIGHT ENABLE
    self.straightReward = QtWidgets.QCheckBox(w)
    self.straightReward.setText(_('Straight Reward'))
    self.gridLayout_straight.addWidget(self.straightReward, 0, 0, 1, 3)

    ##### STRAIGHT LENGTH
    self.straightLengthLabel = QtWidgets.QLabel(w)
    self.straightLengthLabel.setText(_('Straight Length'))
    self.gridLayout_straight.addWidget(self.straightLengthLabel, 1, 0, 1, 3)

    self.straightLengthSpinBox = QtWidgets.QSpinBox(w)
    self.gridLayout_straight.addWidget(self.straightLengthSpinBox, 1, 1, 1, 3)

    ##### START EASE
    self.straightStartEaseLabel = QtWidgets.QLabel(w)
    self.straightStartEaseLabel.setText(_('Start Ease'))
    self.gridLayout_straight.addWidget(self.straightStartEaseLabel, 2, 0, 1, 3)

    self.straightStartEaseSpinBox = QtWidgets.QSpinBox(w)
    self.straightStartEaseSpinBox.setSuffix('%')
    self.gridLayout_straight.addWidget(self.straightStartEaseSpinBox, 2, 1, 1, 3)

    ##### STOP EASE
    self.straightStopEaseLabel = QtWidgets.QLabel(w)
    self.straightStopEaseLabel.setText(_('Stop Ease'))
    self.gridLayout_straight.addWidget(self.straightStopEaseLabel, 3, 0, 1, 3)

    self.straightStopEaseSpinBox = QtWidgets.QSpinBox(w)
    self.straightStopEaseSpinBox.setSuffix('%')
    self.gridLayout_straight.addWidget(self.straightStopEaseSpinBox, 3, 1, 1, 3)

    ##### STEP EASE
    self.straightStepEaseLabel = QtWidgets.QLabel(w)
    self.straightStepEaseLabel.setText(_('Step Ease'))
    self.gridLayout_straight.addWidget(self.straightStepEaseLabel, 4, 0, 1, 3)

    self.straightStepEaseSpinBox = QtWidgets.QSpinBox(w)
    self.straightStepEaseSpinBox.setSuffix('%')
    self.gridLayout_straight.addWidget(self.straightStepEaseSpinBox, 4, 1, 1, 3)

    ##### VERTICAL SPACER
    verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    self.gridLayout_straight.addItem(verticalSpacer)

    w.setLayout(self.gridLayout_straight)
    self.tabWidget.insertTab(2, w, 'Straight Rewards')

def load_reward_tab(self):
    """Get the option for Straight Reward."""
    self.conf = self.mw.col.decks.confForDid(self.deck['id'])
    c = self.conf
    f = self.form
    f.straightReward.setChecked(c.get("straightReward", False))

def save_reward_tab(self):
    """Save the option for Straight Reward."""
    self.conf['straightReward'] = self.form.straightReward.isChecked()

def init_conf():
    dconf.Ui_Dialog.setupUi = wrap(dconf.Ui_Dialog.setupUi, setup_reward_tab)
    DeckConf.loadConf = wrap(DeckConf.loadConf, load_reward_tab)
    DeckConf.saveConf = wrap(DeckConf.saveConf, save_reward_tab, 'before')
