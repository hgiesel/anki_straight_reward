from typing import Any

from aqt import mw

version = "v0.6.1"


class ProfileConfig:
    """Can be used for profile-specific settings"""

    def __init__(self, keyword: str, default: Any):
        self.keyword = keyword
        self.default = default

    @property
    def value(self) -> Any:
        return mw.pm.profile.get(self.keyword, self.default)

    @value.setter
    def value(self, new_value: Any):
        mw.pm.profile[self.keyword] = new_value

    def remove(self):
        try:
            del mw.pm.profile[self.keyword]
        except KeyError:
            # same behavior as Collection.remove_config
            pass


syncDisabled = ProfileConfig("straightRewardOnSyncDisabled", False)
