from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from typing_inspection.typing_objects import target

from app.models.game import GameModel, MobModel
from app.models.room import RoomModel

from app.cruds.room import room_attached_models_crud
from app.game_systems.room.room_handler import handler
from app.game_systems.room.tools import state_manager

from game_data import const
from game_data.templates.items import WeaponItem

"""
    CRUD Interfaces
"""

async def room_home_action(
        game_model: GameModel,
        session: AsyncSession,
) -> str:
    enemies: list[MobModel] = await room_attached_models_crud.get_enemies(
        room_model=game_model.room,
        pointer_const=const.RoomStates.General.TEXT,
        session=session,
    )

    string: str = await handler.home_room_handle(
        game_model=game_model,
        room_model=game_model.room,
        enemies=enemies,
    )
    await _commit_session(enemies, session)

    return string



async def end_player_turn(
        game_model: GameModel,
        session: AsyncSession,
) -> str:
    state_manager.validate_player_turn(game_model.room)

    enemies: list[MobModel] = await room_attached_models_crud.get_enemies(
        room_model=game_model.room,
        pointer_const=const.RoomStates.General.INIT,
        session=session,
    )

    string = await handler.end_player_turn(game_model, enemies)
    await _commit_session(enemies, session)

    return string



async def close_attack_to_select_target(
        game_model: GameModel,
        session: AsyncSession,
) -> str:
    state_manager.validate_player_turn(game_model.room)

    enemies: list[MobModel] = await room_attached_models_crud.get_enemies(game_model.room, const.RoomStates.General.INIT, session)

    weapon: WeaponItem = await room_attached_models_crud.get_close_weapon(game_model, session)

    string: str = await handler.close_attack_to_select_target(
        game_model=game_model,
        room_model=game_model.room,
        enemies=enemies,
        weapon=weapon,
    )
    await _commit_session(enemies, session)

    return string



async def close_attack(
        game_model: GameModel,
        session: AsyncSession,
        target: int | None
) -> str:
    state_manager.validate_player_turn(game_model.room)

    enemies: list[MobModel] = await room_attached_models_crud.get_enemies(game_model.room, const.RoomStates.General.INIT, session)

    weapon: WeaponItem = await room_attached_models_crud.get_close_weapon(game_model, session)

    string: str = await handler.close_attack(
        game_model=game_model,
        room_model=game_model.room,
        enemies=enemies,
        weapon=weapon,
        target=target,
    )
    await _commit_session(enemies, session)

    return string



async def range_attack_to_select_target(
        game_model: GameModel,
        session: AsyncSession,
) -> str:
    state_manager.validate_player_turn(game_model.room)

    enemies: list[MobModel] = await room_attached_models_crud.get_enemies(game_model.room, const.RoomStates.General.INIT, session)

    weapon: WeaponItem | None = await room_attached_models_crud.get_range_weapon(game_model, session)

    string: str = await handler.range_attack_to_select_target(
        game_model=game_model,
        room_model=game_model.room,
        enemies=enemies,
        weapon=weapon,
    )
    await _commit_session(enemies, session)

    return string



async def range_attack(
        game_model: GameModel,
        session: AsyncSession,
        target: int | None
) -> str:
    state_manager.validate_player_turn(game_model.room)

    enemies: list[MobModel] = await room_attached_models_crud.get_enemies(game_model.room, const.RoomStates.General.INIT, session)

    weapon: WeaponItem | None = await room_attached_models_crud.get_range_weapon(game_model, session)

    string: str = await handler.range_attack(
        game_model=game_model,
        room_model=game_model.room,
        enemies=enemies,
        weapon=weapon,
        target=target,
    )
    await _commit_session(enemies, session)

    return string



async def _commit_session(
        enemies: list[MobModel],
        session: AsyncSession
):
    for enemy in enemies:
        if hasattr(enemy, "_delete_label") and enemy._delete_label:
            await session.delete( enemy )

    await session.commit()