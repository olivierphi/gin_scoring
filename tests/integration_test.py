from datetime import datetime
from http import HTTPStatus
from unittest.mock import ANY

import pytest
from django.forms import model_to_dict
from django.test import Client
from django.utils import timezone

from gin_scoring.apps.scoreboard.models import GameResult


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
def test_index(client: Client):
    """Just a smoke test for the moment"""
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert b"Gin Rummy hall of fame" in response.content


@pytest.mark.django_db
def test_post_game_result_happy_path(client: Client):
    """Just a quick smoke test for the moment"""
    data = {
        "player_north_name": "Bob",
        "player_south_name": "Alice",
        "outcome": "gin",
        "winner_name": "Alice",
        "deadwood_value": "6",
    }
    response = client.post("/game/result", data)
    assert response.status_code == HTTPStatus.FOUND

    results_in_db = GameResult.objects.all()
    assert len(results_in_db) == 1
    result_in_db: GameResult = results_in_db[0]

    assert isinstance(result_in_db.created_at, datetime)
    now = timezone.now()
    assert (now - result_in_db.created_at).total_seconds() < 2

    result_as_dict = model_to_dict(result_in_db)
    assert result_as_dict == {
        "id": ANY,
        # Player names are normalised (in lower case)
        # Also, the "north" player is always the first one in alphabetical order
        "player_north_name": "alice",
        "player_south_name": "bob",
        "outcome": "gin",
        "winner_name": "alice",
        "deadwood_value": 6,
        "winner_score": 6 + 25,
        "created_at": ANY,
    }
