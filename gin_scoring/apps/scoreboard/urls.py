from django.urls import path

from . import views

app_name = "scoreboard"
urlpatterns = [
    path("", views.index, name="index"),
    path("ping", views.ping, name="ping"),
    path("login", views.log_in, name="log_in"),
    path("logout", views.log_out, name="log_out"),
]
