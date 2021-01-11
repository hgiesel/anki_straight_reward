from aqt import mw
from aqt.qt import QWidget, QLabel, QSpinBox, QCheckBox, QGridLayout, QVBoxLayout
from aqt.deckconf import DeckConf

from aqt.gui_hooks import (
    deck_conf_did_load_config,
    deck_conf_will_save_config,
    deck_conf_did_setup_ui_form,
)

from ..config import (
    StraightSetting,
    get_setting_from_config,
    serialize_setting,
    deserialize_setting,
    write_setting,
)


def make_label(parent: QWidget, text: str) -> QLabel:
    label = QLabel(parent)
    label.setText(_(text))

    return label


def make_spin_box(
    parent: QWidget, minimum: int = 0, maximum: int = 999, suffix: str = "%"
) -> QSpinBox:
    spinBox = QSpinBox(parent)
    spinBox.setMinimum(minimum)
    spinBox.setMaximum(maximum)
    spinBox.setSuffix(suffix)

    return spinBox


def get_grid_layout(form) -> QWidget:
    w = QWidget()

    gridLayout = QGridLayout()
    gridLayout.setColumnStretch(1, 5)
    gridLayout.setContentsMargins(0, 0, 0, 5)

    ##### STRAIGHT LENGTH
    form.straightLengthLabel = make_label(w, "Begin at straight of length")
    gridLayout.addWidget(form.straightLengthLabel, 1, 0, 1, 1)

    form.straightLengthSpinBox = make_spin_box(w, 0, 100, "")
    gridLayout.addWidget(form.straightLengthSpinBox, 1, 1, 1, 2)

    ##### BASE EASE
    form.straightBaseEaseLabel = make_label(w, "Base ease reward")
    gridLayout.addWidget(form.straightBaseEaseLabel, 2, 0, 1, 1)

    form.straightBaseEaseSpinBox = make_spin_box(w)
    gridLayout.addWidget(form.straightBaseEaseSpinBox, 2, 1, 1, 2)

    ##### STEP EASE
    form.straightStepEaseLabel = make_label(w, "Step ease reward")
    gridLayout.addWidget(form.straightStepEaseLabel, 3, 0, 1, 1)

    form.straightStepEaseSpinBox = make_spin_box(w)
    gridLayout.addWidget(form.straightStepEaseSpinBox, 3, 1, 1, 2)

    ##### START EASE
    form.straightStartEaseLabel = make_label(w, "Start at ease")
    gridLayout.addWidget(form.straightStartEaseLabel, 4, 0, 1, 1)

    form.straightStartEaseSpinBox = make_spin_box(w, 130)
    gridLayout.addWidget(form.straightStartEaseSpinBox, 4, 1, 1, 2)

    ##### STOP EASE
    form.straightStopEaseLabel = make_label(w, "Stop at ease")
    gridLayout.addWidget(form.straightStopEaseLabel, 5, 0, 1, 1)

    form.straightStopEaseSpinBox = make_spin_box(w, 130)
    gridLayout.addWidget(form.straightStopEaseSpinBox, 5, 1, 1, 2)

    w.setLayout(gridLayout)

    return w


def setup_reward_tab(dconf: DeckConf) -> None:
    """Add an option tab for Straight Reward at Review section on Deckconf dialog."""
    w = QWidget()
    form = dconf.form
    form.horizontalLayout_straight = QVBoxLayout()

    ##### GRID LAYOUT
    form.gridLayout_straight = get_grid_layout(form)
    form.horizontalLayout_straight.addWidget(form.gridLayout_straight)

    ##### ENABLE NOTIFICATIONS
    form.straightEnableNotificationsCheckBox = QCheckBox("Enable Notifications", w)
    form.horizontalLayout_straight.addWidget(form.straightEnableNotificationsCheckBox)

    ##### STRETCH
    form.horizontalLayout_straight.addStretch()

    ##### FINISH UP
    w.setLayout(form.horizontalLayout_straight)

    positionBetweenReviewsAndLapses = 2
    form.tabWidget.insertTab(positionBetweenReviewsAndLapses, w, "Rewards")


def load_reward_tab_with_setting(dconf: DeckConf, sett: StraightSetting) -> None:
    f = dconf.form

    f.straightLengthSpinBox.setValue(sett.straight_length)
    f.straightEnableNotificationsCheckBox.setChecked(sett.enable_notifications)
    f.straightBaseEaseSpinBox.setValue(sett.base_ease)
    f.straightStepEaseSpinBox.setValue(sett.step_ease)
    f.straightStartEaseSpinBox.setValue(sett.start_ease)
    f.straightStopEaseSpinBox.setValue(sett.stop_ease)


def load_reward_tab(dconf: DeckConf, _deck, config) -> None:
    """Get the option for Straight Reward."""
    straight_sett = get_setting_from_config(config)
    load_reward_tab_with_setting(dconf, straight_sett)


def get_setting_from_reward_tab(dconf: DeckConf) -> StraightSetting:
    """Save the option for Straight Reward."""
    f = dconf.form

    return deserialize_setting(
        f.straightLengthSpinBox.value(),
        f.straightEnableNotificationsCheckBox.isChecked(),
        f.straightBaseEaseSpinBox.value(),
        f.straightStepEaseSpinBox.value(),
        f.straightStartEaseSpinBox.value(),
        f.straightStopEaseSpinBox.value(),
    )


def save_reward_tab(dconf: DeckConf, _deck, config) -> None:
    setting = get_setting_from_reward_tab(dconf)
    write_setting(config, setting)


def init_deckconf():
    deck_conf_did_setup_ui_form.append(setup_reward_tab)
    deck_conf_did_load_config.append(load_reward_tab)
    deck_conf_will_save_config.append(save_reward_tab)
