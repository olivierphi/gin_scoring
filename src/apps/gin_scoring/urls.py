from django.db.models import Sum, Count
from django.http import HttpRequest
from django.shortcuts import render, redirect
from ninja import NinjaAPI, Form

from .conversion import game_result_data_to_model
from .http_domain import GameResultData
from .models import GameResult

api = NinjaAPI(urls_namespace="html_views")


@api.get("/", url_name="index")
def index(request: HttpRequest):
    last_game_results = GameResult.objects.all().order_by("-created_at")[:10]
    hall_of_fame = (
        GameResult.objects.all()
        .values("winner_name")
        .distinct()
        .annotate(count=Count("winner_score"), total=Sum("winner_score"))
        .order_by("-total")
    )

    return render(
        request, "gin_scoring/index.html", {"last_game_results": last_game_results, "hall_of_fame": hall_of_fame}
    )


@api.post("/game/result", url_name="post_game_result")
def post_game_result(request: HttpRequest, game_result: GameResultData = Form(...)):
    game_result_model = game_result_data_to_model(game_result)
    game_result_model.save()

    return redirect("html_views:index")
