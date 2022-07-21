from http import HTTPStatus

import pydantic
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST, require_safe

from .domain import commands, queries
from .http_payloads import GameResultPayload


@require_safe
def ping(request: HttpRequest) -> HttpResponse:
    return HttpResponse(status=HTTPStatus.NO_CONTENT)


@require_safe
def index(request: HttpRequest) -> HttpResponse:
    last_game_results = queries.last_game_results()
    hall_of_fame = queries.hall_of_fame()
    hall_of_fame_monthly = queries.hall_of_fame_monthly()

    return render(
        request,
        "gin_scoring/index.html",
        {
            "last_game_results": last_game_results,
            "hall_of_fame": hall_of_fame,
            "hall_of_fame_monthly": hall_of_fame_monthly,
        },
    )


@require_POST
def post_game_result(request: HttpRequest) -> HttpResponse:
    try:
        game_result_payload = GameResultPayload(**request.POST.dict())
    except pydantic.ValidationError:
        return HttpResponseBadRequest()

    commands.save_game_result(
        player_north_name=game_result_payload.player_north_name,
        player_south_name=game_result_payload.player_south_name,
        outcome=game_result_payload.outcome,
        winner_name=game_result_payload.winner_name,
        deadwood_value=game_result_payload.deadwood_value,
    )

    return redirect("index")
