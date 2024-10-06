import typing as t

from ...models import GameResult


def last_game_results() -> t.Sequence[GameResult]:
    return t.cast(
        t.Sequence[GameResult], GameResult.objects.all().order_by("-created_at")[:10]
    )
