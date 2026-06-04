from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from game_data import const
from app.cruds.general import profile_crud
from app.cruds.game import game_crud

from app.models.general import ProfileModel
from app.models.game import GameModel, MainCharacterModel, CharEquipModel, InventoryModel
from app.models.world import WorldModel
from app.models.raid import RaidModel, MetaModel
from app.models.room import RoomModel
from app.models.game import RollModel



"""
    Crud Interfaces
"""

async def create_game(
        ip_address: str,
        game_slot: int,
        player_name: str,
        session: AsyncSession,
) -> GameModel:

    # Получение ProfileModel
    profile_model: ProfileModel = await profile_crud.get_profile_by_ip(
        ip_address=ip_address,
        raise_if_none=True,
        session=session
    )

    await _check_free_slot(profile_model, game_slot)

    # Создание GameModel
    main_character = await _create_character(player_name, session)

    world_model = await _create_world(session)

    raid_model = await _create_raid(session)

    room_model = await _create_room(session)

    meta_model = await _create_raid_meta(session)

    roll_model = await _create_roll(session)

    game_model = await _create_game(
        main_character,
        world_model,
        raid_model,
        room_model,
        meta_model,
        roll_model,
        session,
    )

    # Подключаем игру к Profile

    await _connect_game_to_profile(
        profile_model=profile_model,
        game_model=game_model,
        game_slot=game_slot,
        session=session,
    )

    await _set_active_game(
        profile_model=profile_model,
        game_slot=game_slot,
        session=session,
    )

    return game_model



async def set_active_game(
        ip_address: str,
        game_slot: int,
        session: AsyncSession,
) -> int:
    profile_model: ProfileModel = await profile_crud.get_profile_by_ip(
        ip_address=ip_address,
        raise_if_none=True,
        session=session,
    )

    game_id: int = await _set_active_game(
        profile_model=profile_model,
        game_slot=game_slot,
        session=session
    )

    return game_id



async def delete_game(ip_address: str, game_slot: int, session: AsyncSession):
    profile_model: ProfileModel = await profile_crud.get_profile_by_ip(
        ip_address=ip_address,
        raise_if_none=True,
        session=session,
    )

    game_model = await _get_game_by_slot(
        profile_model=profile_model,
        game_slot=game_slot,
        session=session,
    )
    game_id: int = game_model.id

    await _remove_game_from_profile(
        profile_model=profile_model,
        game_slot=game_slot,
        session=session
    )

    await _delete_game(game_model, session)

    return game_id



"""
    Crud Checks
"""


async def _check_free_slot(
        profile_model: ProfileModel,
        game_slot: int,
):
    if game_slot == 1:
        if profile_model.first_game_id is None:
            return

    if game_slot == 2:
        if profile_model.second_game_id is None:
            return

    if game_slot == 3:
        if profile_model.third_game_id is None:
            return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="В данном слоте уже существует экземпляр игры.\n"
               "Прежде чем создавать новую игру в этот слот,\n"
               " нужно удалить игру в этом слоте"
    )



"""
    Crud Realization
"""

async def _create_game(
        main_char: MainCharacterModel,
        world_model: WorldModel,
        raid_model: RaidModel,
        room_model: RoomModel,
        meta_model: MetaModel,
        roll_model: RollModel,
        session: AsyncSession,
) -> GameModel:
    game_model = GameModel(
        character_id=main_char.id,
        world_id=world_model.id,
        raid_id=raid_model.id,
        room_id=room_model.id,
        roll_id=roll_model.id,
        meta_id=meta_model.id,
        major_state=const.WorldState.WORLD,
    )
    session.add( game_model )
    await session.commit()

    return game_model



async def _create_character(
        player_name: str,
        session: AsyncSession,
) -> MainCharacterModel:

    char_equip_model = await _create_char_equipment(session)

    inventory_model = await _create_inventory(session)

    main_character = MainCharacterModel(
        name=player_name,
        char_equip_id=char_equip_model.id,
        inventory_id=inventory_model.id,
    )

    session.add( main_character )
    await session.commit()
    return main_character



async def _create_char_equipment(session: AsyncSession) -> CharEquipModel:
    char_equip_model = CharEquipModel()
    session.add( char_equip_model )
    await session.commit()
    return char_equip_model


async def _create_inventory(session: AsyncSession) -> InventoryModel:
    inventory_model = InventoryModel()
    session.add( inventory_model )
    await session.commit()
    return inventory_model




async def _create_world(
        session: AsyncSession,
) -> WorldModel:
    world_model = WorldModel()
    session.add( world_model )
    await session.commit()
    return world_model



async def _create_raid(
        session: AsyncSession,
) -> RaidModel:
    raid_model = RaidModel()
    session.add(raid_model)
    await session.commit()
    return raid_model



async def _create_room(
        session: AsyncSession,
) -> RoomModel:
    room_model = RoomModel()
    session.add(room_model)
    await session.commit()
    return room_model


async def _create_raid_meta(
        session: AsyncSession,
) -> MetaModel:
    meta_model = MetaModel()
    session.add( meta_model )
    await session.commit()
    return meta_model



async def _create_roll(
        session: AsyncSession,
) -> RollModel:
    roll_model = RollModel()
    session.add( roll_model )
    await session.commit()
    return roll_model



async def _connect_game_to_profile(
        profile_model: ProfileModel,
        game_model: GameModel,
        game_slot: int,
        session: AsyncSession,
):

    if game_slot == 1:
        profile_model.first_game_id = game_model.id
    elif game_slot == 2:
        profile_model.second_game_id = game_model.id
    elif game_slot == 3:
        profile_model.third_game_id = game_model.id

    await session.commit()



async def _set_active_game(
        profile_model: ProfileModel,
        game_slot: int,
        session: AsyncSession,
):
    game_id = None
    if game_slot == 1:
        game_id = profile_model.first_game_id
    elif game_slot == 2:
        game_id = profile_model.second_game_id
    elif game_slot == 3:
        game_id = profile_model.third_game_id

    if game_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Не удалось получить игру в слоте '{game_slot}'"
        )

    profile_model.active_game_id = game_id
    await session.commit()

    return game_id


async def _get_game_by_slot(
        profile_model: ProfileModel,
        game_slot: int,
        session: AsyncSession,
) -> GameModel:

    game_id: int | None = None

    if game_slot == 1:
        game_id = profile_model.first_game_id
    elif game_slot == 2:
        game_id = profile_model.second_game_id
    elif game_slot == 3:
        game_id = profile_model.third_game_id

    if game_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Не удалось получить игру по слоту '{game_slot}'"
        )

    statement = select( GameModel ).where( GameModel.id == game_id )
    result: Result = await session.execute( statement )
    game_model: GameModel = result.scalar_one()

    return game_model



async def _remove_game_from_profile(
        profile_model: ProfileModel,
        game_slot: int,
        session: AsyncSession
):
    game_id: int | None = None
    if game_slot == 1:
        game_id = profile_model.first_game_id
        profile_model.first_game_id = None
    elif game_slot == 2:
        game_id = profile_model.second_game_id
        profile_model.second_game_id = None
    elif game_slot == 3:
        game_id = profile_model.third_game_id
        profile_model.third_game_id = None

    if profile_model.active_game_id == game_id:
        profile_model.active_game_id = None

    await session.commit()



async def _delete_game(game_model: GameModel, session: AsyncSession):
    await session.delete(game_model)
    await session.commit()