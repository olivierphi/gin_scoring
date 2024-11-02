from django.urls import path

from . import views

app_name = "scoreboard"
urlpatterns = [
    path("", views.index, name="index"),
    path("ping", views.ping, name="ping"),
    path("login", views.log_in, name="log_in"),
    path("game/result", views.record_game, name="record_game"),
]
