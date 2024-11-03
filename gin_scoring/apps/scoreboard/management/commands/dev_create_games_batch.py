from django.core.management.base import BaseCommand

from ...dev_helpers import create_test_game


class Command(BaseCommand):
    help = "[dev only] Create a batch of test games"

    def add_arguments(self, parser):
        parser.add_argument(
            "--player-pair-id",
            type=int,
            help="ID of the PlayerPair",
        )
        parser.add_argument(
            "--count",
            type=int,
            required=True,
            help="Number of games to create",
        )

    def handle(
        self,
        *args,
        player_pair_id: int | None,
        count: int,
        **options,
    ):
        for _ in range(count):
            create_test_game(
                player_pair_id=player_pair_id,
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} games."))
