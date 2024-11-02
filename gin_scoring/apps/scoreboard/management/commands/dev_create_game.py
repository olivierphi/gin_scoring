import datetime as dt
from typing import Literal

from django.core.management.base import BaseCommand

from ...dev_helpers import OUTCOMES_AS_STRS, create_test_game


class Command(BaseCommand):
    help = "[dev only] Create a test game"

    def add_arguments(self, parser):
        parser.add_argument(
            "--player-pair-id",
            type=int,
            help="ID of the PlayerPair",
        )
        parser.add_argument(
            "--date",
            type=dt.datetime.fromisoformat,
            help="recording date",
        )
        parser.add_argument(
            "--deadwood",
            type=int,
            help="deadwood value",
        )
        parser.add_argument(
            "--outcome",
            choices=OUTCOMES_AS_STRS,
            help="the game outcome",
        )
        parser.add_argument(
            "--winner",
            choices=["1", "2"],
            help="the winner",
        )

    def handle(
        self,
        *args,
        player_pair_id: int | None,
        date: dt.datetime | None,
        deadwood: int | None,
        outcome: str | None,
        winner: Literal["1", "2"] | None,
        **options,
    ):
        game_result = create_test_game(
            player_pair_id=player_pair_id,
            date=date,
            deadwood=deadwood,
            outcome=outcome,
            winner=winner,
        )

        self.stdout.write(self.style.SUCCESS("Game created successfully"))
        for field_name, field_getter in (
            ("outcome", lambda r: r.get_outcome_display()),
            ("deadwood_value", lambda r: r.deadwood_value),
            ("winner", lambda r: r.winner_name),
            ("winner_score", lambda r: r.winner_score),
            ("created_at", lambda r: r.created_at),
        ):
            self.stdout.write(f"{field_name}: {field_getter(game_result)}")
