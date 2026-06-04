from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game import GameModel

from app.cruds.game import get_game_crud
from app.cruds.game import game_crud



async def home_world(
        ip_address: str,
        session: AsyncSession,
) -> GameModel:
    game_model: GameModel = await get_game_crud.get_active_game(ip_address, session)

    return game_model