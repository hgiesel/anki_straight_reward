from dataclasses import dataclass


@dataclass
class StraightSetting:
    straight_length: int
    enable_notifications: bool
    base_ease: int
    step_ease: int
    start_ease: int
    stop_ease: int
