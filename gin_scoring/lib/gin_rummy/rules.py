from .consts import GameOutcome


def calculate_round_score(*, game_outcome: GameOutcome, deadwood: int) -> int:
    # @link https://en.wikipedia.org/wiki/Gin_rummy#Knocking
    match game_outcome:
        case GameOutcome.DRAW:
            return 0
        case GameOutcome.KNOCK:
            return deadwood
        case GameOutcome.UNDERCUT:
            return 15 + deadwood
        case GameOutcome.GIN:
            return 25 + deadwood
        case GameOutcome.BIG_GIN:
            return 31 + deadwood
        case _:
            raise ValueError(f"Invalid game outcome value '{game_outcome}'")
