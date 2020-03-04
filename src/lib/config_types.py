from dataclasses import dataclass

@dataclass
class StraightSetting:
    deck_conf_name: str
    straight_length: int
    base_ease: int
    step_ease: int
    start_ease: int
    stop_ease: int
