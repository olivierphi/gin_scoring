import pytest
from django.contrib.auth.models import User

from gin_scoring.apps.scoreboard.models import PlayerPair


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        email="",
        password="testpassword",
        is_active=True,
    )


@pytest.fixture
def player_pair(user: User):
    return PlayerPair.objects.create(
        player_1_name="Alice", player_2_name="Bob", user=user
    )
