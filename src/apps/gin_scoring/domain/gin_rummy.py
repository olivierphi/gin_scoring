import typing as t

GAME_OUTCOME = t.Literal["knock", "gin", "big_gin", "draw"]


def calculate_round_score(*, game_outcome: GAME_OUTCOME, deadwood_value: int) -> int:
    # @link https://en.wikipedia.org/wiki/Gin_rummy#Knocking
    match game_outcome:
        case "draw":
            return 0
        case "knock":
            return deadwood_value
        case "gin":
            return 25 + deadwood_value
        case "big_gin":
            return 31 + deadwood_value
        case _:
            raise NotImplementedError(f"Invalid game outcome value '{game_outcome}'")
