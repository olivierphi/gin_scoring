from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("ping", views.ping, name="ping"),
    path("game/result", views.post_game_result, name="post_game_result"),
]
