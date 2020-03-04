import json
from typing import Optional, List
from aqt import mw
from os import path

from .config_types import StraightSetting

from .utils import (
    safenav,
    safenav_preset,
)

SCRIPTNAME = path.dirname(path.realpath(__file__))

with open(path.join(SCRIPTNAME, '../../config.json'), encoding='utf-8') as config:
    config_default = json.load(config)

    SETTINGS_DEFAULT = config_default['settings'][0]
    deck_default = SETTINGS_DEFAULT

    safenav_setting = safenav_preset([deck_default])

def serialize_setting(setting: StraightSetting) -> dict:
    return {
        'deckName': setting.deck_name,
        'lengthOfStraight': setting.length_of_straight,
        'baseEase': setting.base_ease,
        'stepEase': setting.step_ease,
        'startEase': setting.start_ease,
        'stopEase': setting.stop_ease,
    }

def deserialize_setting(deck_name, setting_data, access_func = safenav_setting) -> StraightSetting:
    return setting_data if type(setting_data) == StraightSetting else StraightSetting(
        deck_name,
        access_func([setting_data], ['lengthOfStraight']),
        access_func([setting_data], ['baseEase']),
        access_func([setting_data], ['stepEase']),
        access_func([setting_data], ['startEase']),
        access_func([setting_data], ['stopEase']),

    )

def deserialize_setting_with_default(deck_name, settings):
    found = filter(lambda v: v['deckName'] == deck_name, settings)

    try:
        deck_deserialized = deserialize_setting(deck_name, next(found))

    except StopIteration as e:
        deck_deserialized = deserialize_setting(deck_name, deck_default)

    return deck_deserialized


def get_setting(deck_name='Default', current_config = mw.addonManager.getConfig(__name__)) -> Optional[StraightSetting]:
    return deserialize_setting_with_default(deck_name, safenav([current_config], ['settings'], default=[]))

def get_settings() -> List[StraightSetting]:
    current_config = mw.addonManager.getConfig(__name__)

    deck_settings = [
        get_setting(deck['name'], current_config)
        for deck
        in mw.col.decks.decks.values()
    ]

    return deck_settings

# write config data to config.json
def write_settings(settings: List[StraightSetting]) -> None:
    serialized_settings = [
        serialize_setting(setting)
        for setting
        in settings
    ]

    mw.addonManager.writeConfig(__name__, {
        'settings': serialized_settings,
    })

def write_setting(setting: StraightSetting) -> None:
    current_settings = get_settings()

    mw.addonManager.writeConfig(__name__, {
        'settings': [
            serialize_setting(setting)
            if sett.deck_name == setting.deck_name
            else serialize_setting(sett)
            for sett in current_settings
        ],
    })
