import datetime as dt
import random

from . import models
from .deps import get_db_context
from .security import get_password_hash


async def create_base_fixtures() -> None:
    now = dt.datetime.now()
    async with get_db_context() as session:
        hashed_password = await get_password_hash("test")
        user_1 = models.User(email="test1@test.com", hashed_password=hashed_password)
        player_1_1 = models.Player(name="player_1_1", user=user_1)
        player_1_2 = models.Player(name="player_1_2", user=user_1)

        for i in range(3):
            deadwood_value = random.randint(1, 30)
            game_result = models.GameResult(
                player_north=player_1_1,
                player_south=player_1_2,
                outcome=models.GinRummyOutcome.KNOCK,
                deadwood_value=deadwood_value,
                winner_score=deadwood_value + 15,
                winner=player_1_1 if i % 2 == 0 else player_1_2,
                created_at=now - dt.timedelta(hours=random.randint(1, 1_000)),
            )
            session.add(game_result)

        session.add_all((user_1, player_1_1, player_1_2))

        await session.commit()

        await session.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_base_fixtures())
