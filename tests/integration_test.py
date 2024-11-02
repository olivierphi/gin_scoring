from datetime import datetime
from http import HTTPStatus
from typing import TYPE_CHECKING
from unittest.mock import ANY

import pytest
from django.forms import model_to_dict
from django.test import Client
from django.utils import timezone

from gin_scoring.apps.scoreboard.models import GameResult, GameResultOutcome, PlayerRef

if TYPE_CHECKING:
    from gin_scoring.apps.scoreboard.models import PlayerPair


@pytest.mark.parametrize(
    "method,expected_status_code",
    [
        ("GET", HTTPStatus.NO_CONTENT),
        ("HEAD", HTTPStatus.NO_CONTENT),
        ("POST", HTTPStatus.METHOD_NOT_ALLOWED),
    ],
)
def test_ping(client: Client, method: str, expected_status_code: int):
    response = client.generic(method, "/ping")
    assert response.status_code == expected_status_code


@pytest.mark.django_db
def test_index_anonymous(client: Client):
    """Just a smoke test for the moment"""
    response = client.get("/")
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
def test_log_in(client: Client, player_pair: "PlayerPair"):
    response = client.get("/login")
    assert response.status_code == HTTPStatus.OK
    assert b"Gin Rummy hall of fame" in response.content
    assert b"Log in" in response.content

    user = player_pair.user
    response = client.post(
        "/login", {"username": user.username, "password": "testpassword"}
    )
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == "/"  # type: ignore[attr-defined]

    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert b"Gin Rummy hall of fame" in response.content
    assert b"Log out" in response.content
    assert b"Record game" in response.content
    assert b"Log in" not in response.content


@pytest.mark.django_db
def test_record_new_game_result_happy_path(client: Client, player_pair: "PlayerPair"):
    """Just a quick smoke test for the moment"""
    user = player_pair.user
    client.force_login(user)

    data = {
        "outcome": str(GameResultOutcome.GIN),
        "winner": str(PlayerRef.PLAYER_1),
        "deadwood": "6",
    }
    response = client.post("/", data)
    assert response.status_code == HTTPStatus.FOUND

    results_in_db = GameResult.objects.all()
    assert len(results_in_db) == 1
    result_in_db: GameResult = results_in_db[0]

    assert isinstance(result_in_db.created_at, datetime)
    now = timezone.now()
    assert (now - result_in_db.created_at).total_seconds() < 2

    assert result_in_db.player_pair == player_pair
    assert result_in_db.outcome == GameResultOutcome.GIN
    assert result_in_db.winner_name == "Alice"
    assert result_in_db.deadwood_value == 6
    assert result_in_db.winner_score == 6 + 25
