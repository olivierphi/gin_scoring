import datetime as dt
import sqlite3
from pathlib import Path
from urllib.parse import quote

from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from ...models import GameResult, GameResultOutcome, PlayerPair, PlayerRef

_SOURCE_DB_DATA_READING_SQL = """\
select
    outcome,
    winner_name,
    deadwood_value,
    created_at  
from 
    gin_scoring_gameresult
"""


_OUTCOME_MAPPING: dict[str, GameResultOutcome] = {
    "draw": GameResultOutcome.DRAW,
    "knock": GameResultOutcome.KNOCK,
    "undercut": GameResultOutcome.UNDERCUT,
    "gin": GameResultOutcome.GIN,
    "big_gin": GameResultOutcome.BIG_GIN,
}


class Command(BaseCommand):
    help = "Import game history from the previous format, stored in a SQLite database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--source-db-path",
            type=exiting_path,
            required=True,
            help="The SQLite database file to import from; it will be opened in read-only mode",
        )
        parser.add_argument(
            "--source-db-player-1-name",
            type=str,
            required=True,
            help="Name of the player '1' in the  (case-insensitive)",
        )
        parser.add_argument(
            "--source-db-player-2-name",
            type=str,
            required=True,
            help="Name of the player '2' (case-insensitive)",
        )
        parser.add_argument(
            "--target-player-pair-id",
            type=int,
            required=True,
            help="ID of the PlayerPair that the games will be imported to",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Don't actually import the data, just print what would be done",
        )
        parser.add_argument(
            "--clear-pair-existing-data",
            action="store_true",
        )

    def handle(
        self,
        *args,
        source_db_path: Path,
        source_db_player_1_name: str,
        source_db_player_2_name: str,
        target_player_pair_id: int,
        dry_run: bool,
        clear_pair_existing_data: bool,
        **options,
    ):
        try:
            player_pair = PlayerPair.objects.get(id=target_player_pair_id)
        except PlayerPair.DoesNotExist:
            raise CommandError(
                f"PlayerPair with ID {target_player_pair_id} does not exist"
            )

        if clear_pair_existing_data:
            if dry_run:
                self.stdout.write(
                    self.style.NOTICE("Dry-run mode, didn't clear pair's existing data")
                )
            else:
                GameResult.objects.filter(player_pair=player_pair).delete()
                self.stdout.write("Cleared pair's existing data")

        player_mapping: dict[str, PlayerRef] = {
            source_db_player_1_name.lower(): PlayerRef.PLAYER_1,
            source_db_player_2_name.lower(): PlayerRef.PLAYER_2,
        }

        # We'll open the source database in read-only mode
        con = sqlite3.connect(f"file:{quote(str(source_db_path.resolve()))}?mode=ro")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        # N.B. We won't use `bulk_create` here, as we need to override
        # the `created_at` field - which can't be done with `bulk_create`
        results_counter = 0
        for row in cur.execute(_SOURCE_DB_DATA_READING_SQL):
            outcome = _OUTCOME_MAPPING[row["outcome"]]
            if outcome is not GameResultOutcome.DRAW:
                winner = player_mapping[row["winner_name"].lower()]
            else:
                winner = None
            deadwood = row["deadwood_value"]
            new_result = GameResult(
                player_pair=player_pair,
                outcome=outcome,
                winner=winner,
                deadwood=deadwood,
            )
            results_counter += 1

            if dry_run:
                continue

            new_result.save()

            new_result.created_at = make_aware(
                dt.datetime.fromisoformat(row["created_at"])
            )
            new_result.save(update_fields=["created_at"])

        self.stdout.write(
            f"Processed  {self.style.SUCCESS(str(results_counter))} game results"
        )

        if dry_run:
            self.stdout.write(
                self.style.NOTICE("Dry-run mode, nothing was saved in the database")
            )


def exiting_path(value: str) -> Path:
    path = Path(value)
    if not path.exists():
        raise CommandError(f"Path {path} does not exist")
    return path
