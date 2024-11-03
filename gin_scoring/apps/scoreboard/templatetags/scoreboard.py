import datetime

from django import template
from django.templatetags.static import static

from .. import assets_generation
from ..models import GameResultOutcome

register = template.Library()


@register.simple_tag
def pico_css() -> str:
    return static(
        f"scoreboard/css/{assets_generation.download_assets_if_needed().pico_css_filename}"
    )


@register.simple_tag
def get_possible_outcomes() -> tuple[GameResultOutcome, ...]:
    return tuple(outcome for outcome in GameResultOutcome)
