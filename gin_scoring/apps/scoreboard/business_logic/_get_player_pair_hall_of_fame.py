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
    # @link https://docs.djangoproject.com/en/4.0/topics/db/aggregation/
    wins_count = Count("winner_score")
    total_score = Sum("winner_score")

    hall_of_fame_query_set = (
        GameResult.objects.filter(player_pair=player_pair)
        .filter(winner__isnull=False)
        .values("winner")
        .distinct()
        .annotate(wins_count=wins_count, total_score=total_score)
        # Each won round is worth 25 points:
        .annotate(grand_total=(wins_count * 25) + total_score)
        .order_by("-grand_total")
    )

    draw_games_count = (
        GameResult.objects.filter(player_pair=player_pair)
        .filter(winner__isnull=True)
        .count()
    )

    players_hall_of_fame = tuple(hall_of_fame_query_set)
    total_games_count = (
        sum(row["wins_count"] for row in players_hall_of_fame) + draw_games_count
    )

    previous_total_score = previous_grand_total = 0
    results: list[HallOfFameResult] = []
    for i, row in enumerate(players_hall_of_fame):
        total_score_delta = row["total_score"] - previous_total_score if i > 0 else None
        grand_total_delta = row["grand_total"] - previous_grand_total if i > 0 else None
        results.append(
            HallOfFameResult(
                player=player_pair.get_player_by_ref(row["winner"]),
                wins_count=row["wins_count"],
                wins_percentage=(
                    int(row["wins_count"] / total_games_count * 100)
                    if total_games_count
                    else 0
                ),
                total_score=row["total_score"],
                grand_total=row["grand_total"],
                total_score_delta=total_score_delta,
                grand_total_delta=grand_total_delta,
            )
        )
        previous_total_score = row["total_score"]
        previous_grand_total = row["grand_total"]

    return (
        (results[0], results[1])
        if results
        else (
            get_empty_result(player_pair, PlayerRef.PLAYER_1),
            get_empty_result(player_pair, PlayerRef.PLAYER_2),
        )
    )


def get_empty_result(
    player_pair: "PlayerPair", player_ref: PlayerRef
) -> HallOfFameResult:
    return HallOfFameResult(
        player=player_pair.get_player_by_ref(player_ref),
        wins_count=0,
        wins_percentage=0,
        total_score=0,
        grand_total=0,
        total_score_delta=0,
        grand_total_delta=0,
    )
