from anki.cards import Card
from anki.collection import Collection

from .types import StraightSetting

DEFAULT_SETTINGS = StraightSetting(0, True, 15, 5, 130, 250)
KEYWORD = 'straightReward'

def serialize_setting(setting: StraightSetting) -> dict:
    return {
        'enableNotifications': setting.enable_notifications,
        'straightLength': setting.straight_length,
        'baseEase': setting.base_ease,
        'stepEase': setting.step_ease,
        'startEase': setting.start_ease,
        'stopEase': setting.stop_ease,
    }

def deserialize_setting(
    straight_length: int,
    enable_notifications: bool,
    base_ease: int,
    step_ease: int,
    start_ease: int,
    stop_ease: int,
) -> StraightSetting:
    return StraightSetting(
        straight_length,
        enable_notifications,
        base_ease,
        step_ease,
        start_ease,
        stop_ease,
    )

def deserialize_setting_from_dict(setting_data: dict) -> StraightSetting:
    return StraightSetting(
        setting_data['straightLength'] if 'straightLength' in setting_data else DEFAULT_SETTINGS.straight_length,
        setting_data['enableNotifications'] if 'enableNotifications' in setting_data else DEFAULT_SETTINGS.enable_notifications,
        setting_data['baseEase'] if 'baseEase' in setting_data else DEFAULT_SETTINGS.base_ease,
        setting_data['stepEase'] if 'stepEase' in setting_data else DEFAULT_SETTINGS.step_ease,
        setting_data['startEase'] if 'startEase' in setting_data else DEFAULT_SETTINGS.start_ease,
        setting_data['stopEase'] if 'stopEase' in setting_data else DEFAULT_SETTINGS.stop_ease,
    )

def get_setting_from_config(config) -> StraightSetting:
    try:
        return deserialize_setting_from_dict(config[KEYWORD])
    except:
        return get_default_setting()

def get_setting_from_col(col: Collection, card: Card) -> StraightSetting:
    config = col.decks.confForDid(card.odid or card.did)
    return get_setting_from_config(config)

def get_default_setting() -> StraightSetting:
    return DEFAULT_SETTINGS

def write_setting(col: Collection, config, setting: StraightSetting):
    config[KEYWORD] = serialize_setting(setting)
    col.decks.update_config(config)
