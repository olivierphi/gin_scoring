from django.http import HttpRequest
from django.shortcuts import redirect, render
from ninja import Form, NinjaAPI

from .domain import commands, queries
from .http_payloads import GameResultPayload

api = NinjaAPI(urls_namespace="html_views")


@api.get("/", url_name="index")
def index(request: HttpRequest):
    last_game_results = queries.last_game_results()
    hall_of_fame = queries.hall_of_fame()

    return render(
        request, "gin_scoring/index.html", {"last_game_results": last_game_results, "hall_of_fame": hall_of_fame}
    )


@api.post("/game/result", url_name="post_game_result")
def post_game_result(request: HttpRequest, game_result_payload: GameResultPayload = Form(...)):
    commands.save_game_result(
        player_north_name=game_result_payload.player_north_name,
        player_south_name=game_result_payload.player_south_name,
        outcome=game_result_payload.outcome,
        winner_name=game_result_payload.winner_name,
        deadwood_value=game_result_payload.deadwood_value,
    )

    return redirect("html_views:index")
