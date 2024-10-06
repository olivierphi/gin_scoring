from .consts import GameOutcome


def calculate_round_score(*, game_outcome: GameOutcome, deadwood_value: int) -> int:
    # @link https://en.wikipedia.org/wiki/Gin_rummy#Knocking
    match game_outcome:
        case GameOutcome.DRAW:
            return 0
        case GameOutcome.KNOCK:
            return deadwood_value
        case GameOutcome.UNDERCUT:
            return 15 + deadwood_value
        case GameOutcome.GIN:
            return 25 + deadwood_value
        case GameOutcome.BIG_GIN:
            return 31 + deadwood_value
        case _:
            raise ValueError(f"Invalid game outcome value '{game_outcome}'")
