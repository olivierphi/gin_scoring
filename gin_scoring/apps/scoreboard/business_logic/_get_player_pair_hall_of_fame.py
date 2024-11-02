from typing import TYPE_CHECKING

from django.db.models import Count, Q, Sum

from ..models import GameResult, HallOfFameResult, PlayerRef

if TYPE_CHECKING:
    from ..models import PlayerPair


def get_player_pair_hall_of_fame(
    player_pair: "PlayerPair",
) -> "tuple[HallOfFameResult, HallOfFameResult]":
    """
    The overall "hall of fame" for a player pair, from their very 1st game.
    The winning player comes first in the tuple.
    """
    raw_data = (
        GameResult.objects.filter(player_pair=player_pair)
        .filter(winner__isnull=False)
        .aggregate(
            player_1_score=Sum("winner_score", filter=Q(winner=PlayerRef.PLAYER_1)),
            player_1_wins_count=Count("id", filter=Q(winner=PlayerRef.PLAYER_1)),
            player_2_score=Sum("winner_score", filter=Q(winner=PlayerRef.PLAYER_2)),
            player_2_wins_count=Count("id", filter=Q(winner=PlayerRef.PLAYER_2)),
        )
    )

    games_count = sum(
        (raw_data["player_1_wins_count"], raw_data["player_2_wins_count"])
    )
    player_1_grand_total = raw_data["player_1_score"] + (
        raw_data["player_1_wins_count"] * 25
    )
    player_2_grand_total = raw_data["player_2_score"] + (
        raw_data["player_2_wins_count"] * 25
    )
    if player_1_grand_total > player_2_grand_total:
        player_1_score_delta = None
        player_2_score_delta = -(player_1_grand_total - player_2_grand_total)
    elif player_1_grand_total < player_2_grand_total:
        player_1_score_delta = -(player_2_grand_total - player_1_grand_total)
        player_2_score_delta = None
    else:
        player_1_score_delta = player_2_score_delta = None

    player_1_result = HallOfFameResult(
        winner=PlayerRef.PLAYER_1,
        winner_name=player_pair.player_1_name,
        win_counts=raw_data["player_1_wins_count"],
        win_percentage=(
            int(raw_data["player_1_wins_count"] / games_count * 100)
            if games_count
            else 0
        ),
        total_score=raw_data["player_1_score"],
        grand_total=player_1_grand_total,
        score_delta=player_1_score_delta,
    )
    player_2_result = HallOfFameResult(
        winner=PlayerRef.PLAYER_2,
        winner_name=player_pair.player_2_name,
        win_counts=raw_data["player_2_wins_count"],
        win_percentage=(
            int(raw_data["player_2_wins_count"] / games_count * 100)
            if games_count
            else 0
        ),
        total_score=raw_data["player_2_score"],
        grand_total=player_2_grand_total,
        score_delta=player_2_score_delta,
    )

    hall_of_fame = (
        (player_1_result, player_2_result)
        if player_1_result.grand_total > player_2_result.grand_total
        else (player_2_result, player_1_result)
    )

    return hall_of_fame
