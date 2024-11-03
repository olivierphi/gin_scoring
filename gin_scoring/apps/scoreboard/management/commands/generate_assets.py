from django.core.management.base import BaseCommand

from gin_scoring.apps.scoreboard import assets_generation


class Command(BaseCommand):
    help = "Download the 3rd party assets we rely on (such as a Pico CSS stylesheet)"

    def handle(
        self,
        *args,
        **options,
    ):
        assets_generation.download_assets_if_needed()

        self.stdout.write(self.style.SUCCESS("Assets downloaded successfully"))
