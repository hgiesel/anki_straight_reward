from functools import reduce

def safenav_preset(preset):
    ensure_value = lambda v: v is not None

    def safenav_mod(records, props=[], preds=[], default=None):
        nonlocal preset

        return safenav(
            records + [preset],
            props,
            preds + [ensure_value],
            default,
        )

    return safenav_mod

def safenav(records, props=[], preds=[], default=None):
    nothing = {}

    def access(record, prop):
        nonlocal nothing

        try:
            return record[prop]
        except:
            return nothing

    def find_record(found_record, record):
        nonlocal nothing

        if found_record is not nothing:
            return found_record
        else:
            preresult = reduce(access, props, record)

            def test_preresult(shortcut_value, pred):
                nonlocal preresult
                return shortcut_value and pred(preresult)

            return (preresult
                    if reduce(test_preresult, preds, True)
                    else nothing)

    result = reduce(find_record, records, nothing)
    return default if result is nothing else result

import json
from typing import Optional, List
from aqt import mw
from os import path

from .types import StraightSetting

SCRIPTNAME = path.dirname(path.realpath(__file__))

with open(path.join(SCRIPTNAME, '../config.json'), encoding='utf-8') as config:
    config_default = json.load(config)

    SETTINGS_DEFAULT = config_default['settings']['1'][0]
    deck_default = SETTINGS_DEFAULT

    safenav_setting = safenav_preset(deck_default)

def serialize_setting(setting: StraightSetting) -> dict:
    return {
        # 'deckConfName': setting.deck_conf_name,
        'enableNotifications': setting.enable_notifications,
        'straightLength': setting.straight_length,
        'baseEase': setting.base_ease,
        'stepEase': setting.step_ease,
        'startEase': setting.start_ease,
        'stopEase': setting.stop_ease,
    }

def deserialize_setting(deck_conf_name, setting_data, access_func = safenav_setting) -> StraightSetting:
    result = setting_data if type(setting_data) == StraightSetting else StraightSetting(
        # deck_conf_name,
        access_func([setting_data], ['straightLength']),
        access_func([setting_data], ['enableNotifications']),
        access_func([setting_data], ['baseEase']),
        access_func([setting_data], ['stepEase']),
        access_func([setting_data], ['startEase']),
        access_func([setting_data], ['stopEase']),
    )

    return result

def deserialize_setting_with_default(deck_conf_name, settings) -> StraightSetting:
    found = filter(
        lambda v: safenav([v], ['deckConfName'], default='') == deck_conf_name,
        settings,
    )

    try:
        deck_deserialized = deserialize_setting(deck_conf_name, next(found))

    except StopIteration as e:
        deck_deserialized = deserialize_setting(deck_conf_name, deck_default)

    return deck_deserialized

def get_setting(col, deck_conf_name='Default') -> Optional[StraightSetting]:
    all_config = mw.addonManager.getConfig(__name__)
    setting = safenav(
        [all_config],
        ['settings', str(col.crt)],
        default=[],
    )

    return deserialize_setting_with_default(
        deck_conf_name,
        setting,
    )
