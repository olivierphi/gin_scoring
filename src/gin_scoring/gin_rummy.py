import enum


class GinRummyOutcome(enum.IntEnum):
    """Outcome of a Gin Rummy game."""

    DRAW = 0
    KNOCK = 1
    GIN = 2
