# -*- coding: utf-8 -*-
# Straight Reward:
# an Anki addon increases Ease Factor at every 5 straight success
# ("Good" rating in review).
# Version: 0.0.2
# GitHub: https://github.com/luminousspice/anki-addons/
#
# Copyright: 2019 Luminous Spice <luminous.spice@gmail.com>
#            2020 Henrik Giesel <hengiesel@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

from PyQt5 import QtWidgets, Qt

from anki.sched import Scheduler
from anki.hooks import wrap

from aqt.deckconf import DeckConf
from aqt.forms import dconf
from aqt.utils import tooltip

# Reward at every 5 strait success
STRAIGHT = 5
# Increase +15% to Ease Factor as reward
REWARD = 150
# Praise with the reward.
PRAISE = " Straight Success! <br>Ease Factor gained a %d %% : " %(REWARD/10)

def checkStraight(self, card, conf):
    """Return the latest straight eases from revlog."""
    eases = self.col.db.list(
        "select ease from revlog where cid = ? order by id desc",
        card.id,
    )

    if eases:
        straight = [i for i, x in enumerate(eases) if x < 3]
        if straight:
            return straight[0]
        else:
            return len(eases)

def rescheduleRevReward(self, card, ease):
    """Increase ease factor as reward for straight"""
    dconf = self.col.decks.confForDid(card.did)

    if dconf.get('straitReward'):
        count = checkStraight(self, card, ease)
        if ease == 3 and count > 0 and count % STRAIGHT == STRAIGHT - 1:
            card.factor = max(1300, card.factor+REWARD)
            tooltip(str(count+1) + PRAISE + str(card.factor/10))

def setupUi(self, Dialog):
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
    self.tabWidget.insertTab(2, w, 'Straight Reward')

def load_conf(self):
    """Get the option for Straight Reward."""
    self.conf = self.mw.col.decks.confForDid(self.deck['id'])
    c = self.conf
    f = self.form
    f.straightReward.setChecked(c.get("straightReward", False))

def save_conf(self):
    """Save the option for Straight Reward."""
    self.conf['straightReward'] = self.form.straightReward.isChecked()

Scheduler._rescheduleRev = wrap(Scheduler._rescheduleRev, rescheduleRevReward)
dconf.Ui_Dialog.setupUi = wrap(dconf.Ui_Dialog.setupUi, setupUi)

DeckConf.loadConf = wrap(DeckConf.loadConf, load_conf)
DeckConf.saveConf = wrap(DeckConf.saveConf, save_conf, 'before')
