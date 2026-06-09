from app.models.game import MobModel
from game_data.templates.room import RoomGS
from game_data.templates.entity import BaseEntityGS
from app.game_systems.character import entity_effects

async def init_entity(
        room_gs: RoomGS,
        enemies: list[MobModel | list[MobModel]],
        is_list: bool,
):

    if is_list:
        for model_list, game_schema_list in zip( enemies, room_gs.enemies ):
            for mob_model, entity_gs in zip( model_list, game_schema_list ):
                await _init_mob_model(mob_model, entity_gs)

    else:
        for mob_model, entity_gs in zip( enemies, room_gs.enemies ):
            await _init_mob_model(mob_model, entity_gs)




async def _init_mob_model( mob_model: MobModel, entity_gs_cls: type[BaseEntityGS] ):
    await _init_effect_on_entity(mob_model, entity_gs_cls)



async def _init_effect_on_entity(
        mob_model: MobModel,
        entity_gs_cls: type[BaseEntityGS],
):
    entity_gs = entity_gs_cls()
    for effect_app in entity_gs.effects:
        await entity_effects.add_effect(
            entity=mob_model,
            caster_id=mob_model.id,
            effect_app=effect_app,
        )