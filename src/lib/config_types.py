from dataclasses import dataclass

@dataclass
class StraightSetting:
    deck_name: str
    length_of_straight: int
    base_ease: int
    step_ease: int
    start_ease: int
    stop_ease: int
