from app.models.game import MobModel
from game_data.templates.entity import BaseEntityGS, DropSpec
from game_data.templates.room import RoomGS
from random import randint


async def form_enemies(room_instance: RoomGS, is_list: bool) -> list[MobModel | list[MobModel]]:
    enemies: list[MobModel | list[MobModel]] = await _form_enemies(room_instance, is_list)

    return enemies



async def _form_enemies(room_instance: RoomGS, is_list: bool) -> list[MobModel | list[MobModel]]:

    enemies = []

    if is_list:
        for entity_list in room_instance.enemies:
            buffer_list = []
            for entity_gs_cls in entity_list:
                mob_model = await _create_mob_model(entity_gs_cls)
                buffer_list.append( mob_model )
            enemies.append( buffer_list )

    else:
        for entity_gs_cls in room_instance.enemies:
            mob_model = await _create_mob_model(entity_gs_cls)
            enemies.append( mob_model )


    return enemies



async def _create_mob_model(entity_gs_cls: type[BaseEntityGS]):
    entity_gs = entity_gs_cls()

    mob_model = await _form_mob_model(entity_gs_cls)

    await _define_loot(mob_model, entity_gs)

    mob_model.scripts = [
        "script/enemy/remove_db",
    ]

    return mob_model



async def _form_mob_model(entity_gs_cls: type[BaseEntityGS]) -> MobModel:
    mob_model = MobModel(
        name=entity_gs_cls.name,
        desc=entity_gs_cls.description,

        lvl=entity_gs_cls.lvl,

        hp=randint(entity_gs_cls.min_hp, entity_gs_cls.max_hp),
        mana=randint(entity_gs_cls.min_mana, entity_gs_cls.max_mana),

        actions=entity_gs_cls.actions,
        actions_max=entity_gs_cls.actions_max,
        bonus_actions=entity_gs_cls.bonus_actions,
        bonus_actions_max=entity_gs_cls.bonus_actions_max,

        stat_strength=entity_gs_cls.stat_strength,
        stat_dexterity=entity_gs_cls.stat_dexterity,
        stat_constitution=entity_gs_cls.stat_constitution,
        stat_intelligence=entity_gs_cls.stat_intelligence,
        stat_will=entity_gs_cls.stat_will,
    )

    return mob_model



async def _define_loot(mob_model: MobModel, entity_gs: BaseEntityGS):
    loot = []

    for drop_spec in entity_gs.loot:
        loot += drop_spec.execute()

    mob_model.loot = loot


