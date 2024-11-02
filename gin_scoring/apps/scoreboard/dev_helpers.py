import datetime as dt
import random
from typing import Literal

from django.conf import settings
from django.contrib.auth.models import User

from gin_scoring.lib.gin_rummy.rules import calculate_round_score

from .models import GAME_OUTCOMES_MAPPING, GameResult, GameResultOutcome, PlayerPair

_OUTCOME_MAPPING: dict[str, GameResultOutcome] = {
    "draw": GameResultOutcome.DRAW,
    "knock": GameResultOutcome.KNOCK,
    "undercut": GameResultOutcome.UNDERCUT,
    "gin": GameResultOutcome.GIN,
    "big_gin": GameResultOutcome.BIG_GIN,
}
OUTCOMES_AS_STRS = tuple(_OUTCOME_MAPPING.keys())

_RANDOM_OUTCOMES = (
    # Will create "knocks" most of the time:
    "knock",
    "knock",
    "knock",
    "knock",
    "knock",
    "knock",
    "draw",
    "undercut",
    "gin",
    "big_gin",
)


def create_test_game(
    player_pair_id: int | None = None,
    date: dt.datetime | None = None,
    deadwood: int | None = None,
    outcome: str | None = None,
    winner: Literal["1", "2"] | None = None,
) -> GameResult:
    if not settings.DEBUG:
        raise RuntimeError("This helper is only available in DEBUG mode")

    if player_pair_id is None:
        player_pair = PlayerPair.objects.order_by("?").first()
        if player_pair is None:
            if (user := User.objects.order_by("?").first()) is None:
                raise ValueError("No users found")
            player_pair = PlayerPair.objects.create(
                user=user,
                player_1_name="Rachel",
                player_2_name="Olivier",
            )
    else:
        player_pair = PlayerPair.objects.get(id=player_pair_id)

    if date is None:
        date = dt.datetime.now() - dt.timedelta(days=random.randint(1, 365))
    if date.time() == dt.time.min:
        date = date.replace(
            hour=random.randint(0, 23),
            minute=random.randint(0, 59),
            second=random.randint(0, 59),
        )
    date_utc = date.astimezone(dt.timezone.utc)

    if deadwood is None:
        deadwood = random.randint(1, 20)

    if outcome is None:
        outcome = random.choice(_RANDOM_OUTCOMES)
    game_outcome = _OUTCOME_MAPPING[outcome]

    if game_outcome is GameResultOutcome.DRAW:
        winner = None
    elif winner is None:
        winner = random.choice(("1", "2"))

    game_result = GameResult.objects.create(
        player_pair=player_pair,
        deadwood_value=deadwood,
        outcome=game_outcome,
        winner=int(winner) if winner is not None else None,
    )

    game_result.created_at = game_result.updated_at = date_utc
    game_result.save(update_fields=["created_at", "updated_at"])

    return game_result
