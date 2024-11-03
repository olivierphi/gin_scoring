import enum


@enum.unique
class GameOutcome(enum.Enum):
    KNOCK = "knock"
    GIN = "gin"
    BIG_GIN = "big_gin"
    UNDERCUT = "undercut"
    DRAW = "draw"
