from flask import Blueprint, render_template
from .domain import queries

bp = Blueprint("gin_scoring", __name__)


@bp.route("/ping", methods=("GET", "HEAD"))
def ping():
    return ("", 204)


@bp.route("/ping", methods=("GET", "HEAD"))
def home():

    last_game_results = queries.last_game_results()
    hall_of_fame = [] # queries.hall_of_fame()
    hall_of_fame_monthly = [] # queries.hall_of_fame_monthly()

    return render_template(
        "gin_scoring/index.html",
        **{
            "last_game_results": last_game_results,
            "hall_of_fame": hall_of_fame,
            "hall_of_fame_monthly": hall_of_fame_monthly,
        },
    )
