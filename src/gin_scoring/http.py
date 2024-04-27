from typing import Union

from fastapi import FastAPI
from sqladmin import Admin, ModelView
from .db import engine
from .models import GameResult


app = FastAPI()
admin = Admin(app, engine)


class GameResultAdmin(ModelView, model=GameResult):  # type: ignore[call-arg]
    column_list = (GameResult.id, GameResult.player_north_name)


admin.add_view(GameResultAdmin)


@app.get("/")
async def read_root():
    return {"Hello": "World!"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
