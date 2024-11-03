from http import HTTPStatus
from typing import TYPE_CHECKING

from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, resolve_url
from django.utils.html import escape
from django.views.decorators.http import (
    require_http_methods,
    require_POST,
    require_safe,
)

from .forms import LoginForm, NewGameResultForm
from .models import GameResult, PlayerPair
from .view_helpers import get_player_pair_from_request

if TYPE_CHECKING:
    from django.http import HttpRequest


@require_safe
def ping(request: "HttpRequest") -> HttpResponse:
    return HttpResponse(status=HTTPStatus.NO_CONTENT)


@require_http_methods(["GET", "POST"])
def index(request: "HttpRequest") -> HttpResponse:
    try:
        player_pair = get_player_pair_from_request(request)
    except (ValueError, PlayerPair.DoesNotExist):
        return redirect("scoreboard:log_in")

    if request.method == "POST":
        form = NewGameResultForm(request.POST)
        if form.is_valid():
            GameResult.objects.create(
                player_pair=player_pair,
                deadwood=form.cleaned_data["deadwood"],
                outcome=form.cleaned_data["outcome"],
                winner=form.cleaned_data["winner"],
            )
            return HttpResponseRedirect(
                f"{resolve_url('scoreboard:index')}#monthly-hall-of-fame"
            )
    else:
        form = NewGameResultForm()

    last_game_results = GameResult.objects.get_player_pair_last_game_results(
        player_pair
    )
    hall_of_fame = GameResult.objects.get_player_pair_hall_of_fame(player_pair)
    hall_of_fame_monthly = GameResult.objects.get_player_pair_hall_of_fame_monthly(
        player_pair
    )

    return render(
        request,
        "scoreboard/index.html",
        {
            "form": form,
            "players": player_pair.players,
            "last_game_results": last_game_results,
            "hall_of_fame": hall_of_fame,
            "hall_of_fame_monthly": hall_of_fame_monthly,
        },
    )


@require_http_methods(["GET", "POST"])
def log_in(request: "HttpRequest") -> HttpResponse:
    invalid_credentials = False

    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {escape(user.username)}!")

            return redirect("scoreboard:index")
        else:
            invalid_credentials = True
    else:
        form = LoginForm(request)

    return render(
        request,
        "scoreboard/log-in.html",
        {
            "form": form,
            "invalid_credentials": invalid_credentials,
        },
    )


@require_POST
def log_out(request: "HttpRequest") -> HttpResponse:
    logout(request)
    messages.success(request, "You have been logged out.")

    return redirect("scoreboard:log_in")
