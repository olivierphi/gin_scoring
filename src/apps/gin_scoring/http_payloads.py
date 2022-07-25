from typing import Any

import pydantic

from .domain.gin_rummy import GAME_OUTCOME
from .helpers import normalize_player_name


class GameResultPayload(pydantic.BaseModel):
    player_north_name: str
    player_south_name: str
    outcome: GAME_OUTCOME
    winner_name: str | None
    deadwood_value: int

    @pydantic.root_validator(pre=True)
    def normalize_player_names(cls, values: dict[str, Any]):
        # In order to have consistent recording when players "Rachel" and "Olivier" add a game result, whether
        # "Rachel" is "north" and "Olivier" is "south" or vice-versa, we sort their names alphabetically
        # and then always set the "north" player to the first one and the "south" one to the second one:
        player_north_name, player_south_name = sorted(
            (
                normalize_player_name(values["player_north_name"]),
                normalize_player_name(values["player_south_name"]),
            )
        )
        values["player_north_name"] = player_north_name
        values["player_south_name"] = player_south_name
        return values

    @pydantic.validator("winner_name")
    def validate_winner_name(cls, v: str, values: dict[str, Any]) -> str | None:
        is_draw = values["outcome"] == "draw"

        if is_draw:
            return None  # No winner name for "draw" games

        if not v:
            raise ValueError(f"non-draw games must have a winner name")
        winner_name = normalize_player_name(v)
        player_names = (values["player_north_name"], values["player_south_name"])
        if winner_name not in player_names:
            raise ValueError(f"winner name {v} is not part of the players' names '{','.join(player_names)}'")

        return winner_name
