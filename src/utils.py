from enum import IntEnum

version = "v0.1"

class Answer(IntEnum):
    AGAIN = 1
    HARD = 2
    GOOD = 3
    EASY = 4

class RevlogType(IntEnum):
    LRN = 0
    REV = 1
    RELRN = 2
    EARLYREV = 3
