from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game import GameModel

from app.cruds.game import game_crud

from game_data import const

"""
    CRUD Interfaces
"""

async def try_exit(
        game_model: GameModel,
        session: AsyncSession,
) -> str | None:
    return await _try_exit(game_model, session)


"""
    CRUD Realization
"""


async def _try_exit(
        game_model: GameModel,
        session: AsyncSession,
):
    if game_model.room.can_exit:

        if game_model.raid.current_line < len(game_model.raid.mesh):
            await _step_into_raid(game_model, session)
        else:
            await _step_out_of_raid(game_model, session)



async def _step_into_raid(
        game_model: GameModel,
        session: AsyncSession,
):
    await game_crud.set_major_state_game_model(
        game_model=game_model,
        state=const.WorldState.RAID,
        session=session,
    )

    game_model.raid.current_line += 1
    await session.commit()


async def _step_out_of_raid(
        game_model: GameModel,
        session: AsyncSession,
):
    await game_crud.set_major_state_game_model(
        game_model=game_model,
        state=const.WorldState.WORLD,
        session=session,
    )
