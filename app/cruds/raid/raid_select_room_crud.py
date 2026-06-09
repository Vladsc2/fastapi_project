from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game import GameModel, MobModel
from app.models.raid import RaidModel
from app.models.room import RoomModel

from app.cruds.game import game_crud
from app.game_systems.room.init import room_creator
from app.game_systems.room.init import mob_creator
from app.game_systems.room.init import mob_initer
from app.schemas.room import RoomMeshSchema

from game_data import const
from game_data.templates.room import RoomGS
from game_data.templates.entity import BaseEntityGS


"""
    CRUD Interfaces
"""

async def select_room(
        game_model: GameModel,
        room_number: int,
        session: AsyncSession,
):
    # Получаем RoomMeshSchema из словаря, в mesh рейда
    room_schema: RoomMeshSchema = await _get_selected_room_schema(
        game_model=game_model,
        room_number=room_number,
    )

    await _select_room(
        game_model=game_model,
        room_schema=room_schema,
        session=session,
    )



"""
    CRUD Realization
"""

async def _get_selected_room_schema(
        game_model: GameModel,
        room_number: int,
) -> RoomMeshSchema:
    room_index = room_number - 1

    raid_model: RaidModel = game_model.raid
    mesh: list[list[dict]] = raid_model.mesh

    line = mesh[raid_model.current_line-1]

    if room_index < 0 or room_index >= len(line):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Недоступный номер комнаты\n"
        )

    room_dict = line[room_index]
    room_schema = RoomMeshSchema( **room_dict )

    return room_schema



async def _select_room(
        game_model: GameModel,
        room_schema: RoomMeshSchema,
        session: AsyncSession,
) -> RoomModel:
    # Получаем room_gs (instance), и обновляем room_model согласно room_gs
    room_gs: RoomGS | None = await room_creator.update_room_model(
        room_model=game_model.room,
        room_schema=room_schema,
    )

    # В зависимости от типа локации, используем дополнительные действия
    if room_schema.room_type == const.RoomTypes.BATTLE and room_gs is not None:
        await _form_mob_models(game_model, room_gs, session)
    await session.commit()

    await game_crud.set_major_state_game_model(
        game_model=game_model,
        state=const.WorldState.ROOM,
        session=session
    )




async def _form_mob_models(
        game_model: GameModel,
        room_gs: RoomGS,
        session: AsyncSession,
):
    if len(room_gs.enemies) == 0:
        return
    is_list = isinstance(room_gs.enemies[0], list)
    # Получаем MobModel модели алхимии используя BaseEntityGS внутри room_gs
    enemies: list[MobModel | list[MobModel]] = await mob_creator.form_enemies(room_gs, is_list)
    # Добавляем их в базу данных, и оставляем ссылки на них по id в player_char
    await _append_enemies(
        room_gs=room_gs,
        room_model=game_model.room,
        enemies=enemies,
        is_list=is_list,
        session=session,
    )
    # Инициализируем в mob_model все, где требуется mob_model.id
    await mob_initer.init_entity(
        room_gs=room_gs,
        enemies=enemies,
        is_list=is_list,
    )


async def _append_enemies(
        room_gs: RoomGS,
        room_model: RoomModel,
        enemies: list[MobModel | list[MobModel]],
        is_list: bool,
        session: AsyncSession
):

    if is_list:
        for enemy_list in enemies:
            for mob_model in enemy_list:
                session.add(mob_model)
        await session.commit()

        enemies_id = []
        for enemy_list in enemies:
            buffer_list_id = []
            for mob_model in enemy_list:
                buffer_list_id.append( mob_model.id )
            enemies_id.append( buffer_list_id )


    else:
        for mob_model in enemies:
            session.add(mob_model)
        await session.commit()

        enemies_id = []
        for mob_model in enemies:
            enemies_id.append( mob_model.id )


    room_model.enemies = enemies_id

    await session.commit()

