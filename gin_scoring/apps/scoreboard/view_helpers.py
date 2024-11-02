from typing import TYPE_CHECKING, cast

from .models import PlayerPair

if TYPE_CHECKING:
    from django.contrib.auth.models import User
    from django.http import HttpRequest


def get_player_pair_from_request(request: "HttpRequest") -> PlayerPair:
    user = cast("User", request.user)
    if user.is_anonymous:
        raise ValueError("User is anonymous")

    return PlayerPair.objects.get(user=user)
