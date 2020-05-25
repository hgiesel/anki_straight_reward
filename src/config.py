from dataclasses import fields

from aqt import mw
from anki.cards import Card

from .config_legacy import get_setting as get_legacy
from .types import StraightSetting

DEFAULT_SETTINGS = StraightSetting(0, True, 15, 5, 130, 250)
KEYWORD = 'straightReward'

def fromdict(klass, d):
    try:
        fieldtypes = {
            f.name: f.type for f in fields(klass)
        }

        return klass(**{
            f: fromdict(fieldtypes[f], d[f]) for f in d
        })

    except:
        return d # Not a dataclass field

def sanity_check(conf: any) -> StraightSetting:
    if KEYWORD not in conf:
        return get_legacy(mw.col, conf['name'])

    conf_val = conf[KEYWORD]

    if type(conf_val) != dict:
        return get_legacy(mw.col, conf['name'])

    return fromdict(StraightSetting, {
        'straight_length': conf_val['straight_length'] if 'straight_length' in conf_val else DEFAULT_SETTINGS.straight_length,
        'enable_notifications': conf_val['enable_notifications'] if 'enable_notifications' in conf_val else DEFAULT_SETTINGS.enable_notifications,
        'base_ease': conf_val['base_ease'] if 'base_ease' in conf_val else DEFAULT_SETTINGS.base_ease,
        'step_ease': conf_val['step_ease'] if 'step_ease' in conf_val else DEFAULT_SETTINGS.step_ease,
        'start_ease': conf_val['start_ease'] if 'start_ease' in conf_val else DEFAULT_SETTINGS.start_ease,
        'stop_ease': conf_val['stop_ease'] if 'stop_ease' in conf_val else DEFAULT_SETTINGS.stop_ease,
    })

def get_setting_from_conf(conf) -> StraightSetting:
    result = sanity_check(conf)
    return result

def get_setting(card: Card) -> StraightSetting:
    conf = mw.col.decks.confForDid(card.odid or card.did)
    return get_setting_from_conf(conf)

def get_default_setting() -> StraightSetting:
    return DEFAULT_SETTINGS
