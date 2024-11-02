from random import choices
from typing import TYPE_CHECKING, Literal, TypedDict

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import GameResultOutcome, PlayerRef


class LoginForm(AuthenticationForm):
    pass


class NewGameResultForm(forms.Form):
    outcome = forms.ChoiceField(choices=GameResultOutcome)
    winner = forms.ChoiceField(choices=PlayerRef, required=False)
    deadwood = forms.IntegerField(min_value=0, max_value=100, required=False)

    def clean(self):
        cleaned_data = super().clean()

        outcome = GameResultOutcome(int(cleaned_data["outcome"]))
        cleaned_data["outcome"] = outcome

        if outcome is GameResultOutcome.DRAW:
            cleaned_data["winner"] = None
            cleaned_data["deadwood"] = 0
        else:
            winner_raw = cleaned_data.get("winner")
            winner = PlayerRef(int(winner_raw)) if winner_raw else None
            cleaned_data["winner"] = winner
            deadwood = cleaned_data.get("deadwood")
            if not winner:
                self.add_error("winner", "Winner must be specified")
            if deadwood is None:
                self.add_error("deadwood", "Deadwood value must be specified")

        return cleaned_data

    if TYPE_CHECKING:

        class CleanedDataDraw(TypedDict):
            outcome: Literal[GameResultOutcome.DRAW]
            winner: None
            deadwood: Literal[0]

        class CleanedDataNonDraw(TypedDict):
            outcome: Literal[
                GameResultOutcome.KNOCK,
                GameResultOutcome.UNDERCUT,
                GameResultOutcome.GIN,
                GameResultOutcome.BIG_GIN,
            ]
            winner: PlayerRef
            deadwood: int

        @property
        def cleaned_data(self) -> CleanedDataDraw | CleanedDataNonDraw:  # type: ignore[override]
            raise NotImplementedError
