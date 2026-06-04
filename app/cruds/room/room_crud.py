from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game import GameModel
from app.models.room import RoomModel

from app.cruds.game import game_crud
from app.cruds.room.room_types import battle_room_crud
from game_data import const


"""
    CRUD Interfaces
"""


async def home_action(
        game_model: GameModel,
        session: AsyncSession,
) -> str:
    room_model: RoomModel = game_model.room

    if room_model.room_type == const.RoomTypes.BATTLE:
        string = await battle_room_crud.room_home_action(
            game_model=game_model,
            session=session,
        )

    else:
        string = await _set_can_exit(
            room_model=game_model.room,
            session=session
        )

    return string



"""
    CRUD Realization
"""

async def _set_can_exit(
        room_model: RoomModel,
        session: AsyncSession
) -> str:
    room_model.can_exit = True
    await session.commit()

    return f"""
        Комната с типом '{room_model.room_type}' не обрабатывается
        
         app/cruds/room/room_crud.py
         
        Значение для выхода из локации установлено как True 
        
         <a href="/room/exit">Выйти</a>
    """
