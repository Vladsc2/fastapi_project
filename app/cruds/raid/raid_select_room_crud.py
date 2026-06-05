from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game import GameModel, MobModel
from app.models.raid import RaidModel
from app.models.room import RoomModel

from app.cruds.game import game_crud
from app.game_systems.room.enter_leave import room_creator
from app.schemas.room import RoomMeshSchema

from game_data import const
from game_data.templates.room import RoomGS
from game_data.templates.entity import BaseEntityGS

from app.game_systems.character import entity_effects


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
    room_instance: RoomGS | None = await room_creator.update_room_model(
        room_model=game_model.room,
        room_schema=room_schema,
    )
    await session.commit()


    if room_schema.room_type == const.RoomTypes.BATTLE and room_instance is not None:
        enemies = await room_creator.form_enemies(room_instance)
        await _append_enemies(
            room_gs=room_instance,
            room_model=game_model.room,
            enemies=enemies,
            session=session,
        )


    await game_crud.set_major_state_game_model(
        game_model=game_model,
        state=const.WorldState.ROOM,
        session=session
    )

    await session.commit()





async def _append_enemies(
        room_gs: RoomGS,
        room_model: RoomModel,
        enemies: list[MobModel | list[MobModel]],
        session: AsyncSession
):
    if len(enemies) == 0:
        return

    is_list = isinstance(enemies[0], list)

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

    await _init_effects_on_entities(
        room_gs=room_gs,
        room_model=room_model,
        enemies=enemies,
        is_list=is_list,
    )

    await session.commit()


async def _init_effects_on_entities(
        room_gs: RoomGS,
        room_model: RoomModel,
        enemies: list[MobModel | list[MobModel]],
        is_list: bool,
):
    if is_list:
        for model_list, game_schema_list in zip( enemies, room_gs.enemies ):
            for mob_model, entity_gs in zip( model_list, game_schema_list ):
                await _init_effect_on_entity(mob_model, entity_gs)

    else:
        for mob_model, entity_gs in zip( enemies, room_gs.enemies ):
            await _init_effect_on_entity(mob_model, entity_gs)



async def _init_effect_on_entity(
        mob_model: MobModel,
        entity_gs: BaseEntityGS,
):
    entity_gs_instance = entity_gs()
    for effect_app in entity_gs_instance.effects:
        await entity_effects.add_effect(
            entity=mob_model,
            caster_id=mob_model.id,
            effect_app=effect_app,
        )