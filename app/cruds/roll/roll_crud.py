from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession, result

from app.models.game import GameModel
from app.models.game import RollModel

from app.game_systems.roll import roll_by_const, roll_tools

from game_data import const

"""
    CRUD Interfaces
"""


async def roll_by_constant(
        game_model: GameModel,
        roll_const: str,
        times: int,
        session: AsyncSession,
):
    roll_model: RollModel = game_model.roll

    for i in range(times):
        result = roll_by_const(roll_const)

        roll_tools.update_roll_model_by_const(
            roll_model=roll_model,
            roll_const=roll_const,
            value=result,
        )

    await session.commit()


async def save_back_url_if_not_roll(
        game_model: GameModel,
        back_url: str | None,
        session: AsyncSession,
):
    if back_url is None:
        return
    if "/roll?dice=" in back_url:
        return

    roll_model: RollModel = game_model.roll
    roll_model.back_url = back_url

    await session.commit()



"""
    CRUD Realization
"""

