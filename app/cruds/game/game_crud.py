from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game import GameModel

from app.cruds.game import get_game_crud


"""
    Crud Interfaces
"""

# Set major_state
async def set_major_state_ip(ip_address: str, state: str, session: AsyncSession):
    game_model: GameModel = await get_game_crud.get_active_game(ip_address, session)

    await set_major_state_game_model(game_model, state, session)


async def set_major_state_game_model(game_model: GameModel, state: str, session: AsyncSession):
    await _set_major_state(game_model, state, session)



# Validate major_state
async def validate_major_state(ip_address: str, state: str, session: AsyncSession) -> GameModel:
    game_model: GameModel = await get_game_crud.get_active_game(ip_address, session)

    await _validate_major_state(game_model, state)

    return game_model



# Chack major_state
async def check_major_state_ip(ip_address: str, state: str, session: AsyncSession) -> bool:
    game_model: GameModel = await get_game_crud.get_active_game(ip_address, session)

    return await check_major_state_game_model(game_model, state)


async def check_major_state_game_model(game_model: GameModel, state: str) -> bool:
    return await _check_major_state(game_model, state)


"""
    Crud Checks
"""




"""
    Crud Realization
"""

async def _validate_major_state(game_model: GameModel, state: str):
    if state != game_model.major_state:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Страница с типом '{state}' недоступна\n"
                   f"\n"
                   f"Сейчас в игре установлено состояние '{game_model.major_state}'"
        )


async def _set_major_state(game_model: GameModel, state: str, session: AsyncSession):
    game_model.major_state = state
    await session.commit()


async def _check_major_state(game_model: GameModel, state: str) -> bool:
    return game_model.major_state == state
