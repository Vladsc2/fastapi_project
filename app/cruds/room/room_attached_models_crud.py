from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game import GameModel, MobModel
from app.models.room import RoomModel

from game_data.items import items_system
from game_data.templates.items import WeaponItem

from app.game_systems.room.tools import state_manager
from game_data import const


"""
    CRUD Interfaces
"""

async def get_enemies(
        room_model: RoomModel,
        pointer_const: str,
        session: AsyncSession,
) -> list[MobModel]:
    return await _get_enemies(
        room_model=room_model,
        pointer_const=pointer_const,
        session=session,
    )


async def get_close_weapon(
        game_model: GameModel,
        session: AsyncSession,
) -> WeaponItem:
    return await _get_close_weapon(game_model, session)


async def get_range_weapon(
        game_model: GameModel,
        session: AsyncSession,
) -> WeaponItem | None:
    return await _get_range_weapon(game_model, session)



"""
    CRUD Realization
"""

async def _get_enemies(
        room_model: RoomModel,
        pointer_const: str,
        session: AsyncSession,
) -> list[MobModel]:
    if len(room_model.enemies) == 0:
        return []

    is_int = isinstance(room_model.enemies[0], int)

    mobs = []

    if is_int:
        for mob_id in room_model.enemies:
            mob_model = await _get_one_enemy(mob_id, session)
            mobs.append( mob_model )

    else:
        # Так как pointer_const - это номер завершенного состояния (например TEXT: 2),
        # отнимаем 1 чтобы превратить в указатель на entity_list
        pointer = state_manager.get_state_value(room_model, pointer_const) - 1
        if pointer > len(room_model.enemies):
            return []
        # Отнимаем еще 1, чтобы привести к индексу
        for mob_id in room_model.enemies[pointer-1]:
            mob_model = await _get_one_enemy(mob_id, session)
            mobs.append( mob_model )

    return mobs



async def _get_one_enemy(
        enemy_id: int,
        session: AsyncSession,
) -> MobModel | None:
    statement = select( MobModel ).where( MobModel.id == enemy_id )
    result: Result = await session.execute( statement )
    mob_model = result.scalar_one_or_none()

    return mob_model



async def _get_close_weapon(
        game_model: GameModel,
        session: AsyncSession,
) -> WeaponItem:
    player_char = game_model.character
    equipment = player_char.char_equip

    fists_url = "item/weapon/base_fists"
    if equipment.close_weapon_url == "":
        weapon = items_system.get_item_by_url( fists_url )
    else:
        weapon = items_system.get_item_by_url( equipment.close_weapon_url )
        if weapon is None:
            weapon = items_system.get_item_by_url( fists_url )

    return weapon


async def _get_range_weapon(
        game_model: GameModel,
        session: AsyncSession,
) -> WeaponItem | None:
    player_char = game_model.character
    equipment = player_char.char_equip

    if equipment.range_weapon_url == "":
        return None

    weapon = items_system.get_item_by_url( equipment.range_weapon_url )

    return weapon