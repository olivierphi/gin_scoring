from django.utils.timezone import now

from .gin_rummy import calculate_round_score
from .http_domain import GameResultData
from .models import GameResult


def game_result_data_to_model(game_result: GameResultData) -> GameResult:
    winner_name = None
    winner_score = None
    if not game_result.is_draw:
        winner_name = game_result.winner_name
        winner_score = calculate_round_score(
            game_outcome=game_result.outcome, deadwood_value=game_result.deadwood_value
        )

    return GameResult(
        player_north_name=game_result.player_north_name,
        player_south_name=game_result.player_south_name,
        outcome=game_result.outcome,
        winner_name=winner_name,
        deadwood_value=game_result.deadwood_value,
        winner_score=winner_score,
        created_at=now(),
    )
