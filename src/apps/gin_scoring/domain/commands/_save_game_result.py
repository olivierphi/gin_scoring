import typing as t

from django.utils.timezone import now

from ...domain.gin_rummy import GAME_OUTCOME, calculate_round_score
from ...models import GameResult


def save_game_result(
    player_north_name: str,
    player_south_name: str,
    outcome: GAME_OUTCOME,
    winner_name: t.Optional[str],
    deadwood_value: int,
) -> GameResult:
    is_draw = outcome == "draw"

    winner_score = None
    if is_draw:
        winner_name = None
    else:
        winner_name = winner_name
        winner_score = calculate_round_score(game_outcome=outcome, deadwood_value=deadwood_value)

    game_result_model = GameResult(
        player_north_name=player_north_name,
        player_south_name=player_south_name,
        outcome=outcome,
        winner_name=winner_name,
        deadwood_value=deadwood_value,
        winner_score=winner_score,
        created_at=now(),
    )
    game_result_model.save()

    return game_result_model
