from app.models.room import RoomModel
from app.models.game import MobModel
from app.schemas.room import RoomMeshSchema
from game_data.templates.room import RoomGS
from game_data.templates.entity import BaseEntityGS
from tools.pars import importer
from random import randint


async def update_room_model(room_model: RoomModel, room_schema: RoomMeshSchema) -> RoomGS | None:
    await _update_room_model(room_model, room_schema)

    if room_model.room_path != "":
        room_instance: RoomGS = await _update_room_model_by_file(room_model)
        return room_instance

    return None



async def form_enemies(room_instance: RoomGS) -> list[MobModel]:
    enemies: list[MobModel | list[MobModel]] = await _form_enemies(room_instance)

    return enemies




async def _form_enemies(room_instance: RoomGS) -> list[MobModel | list[MobModel]]:
    if len(room_instance.enemies) == 0:
        return []

    is_list = isinstance(room_instance.enemies[0], list)

    enemies = []

    if is_list:
        for entity_list in room_instance.enemies:
            buffer_list = []
            for entity in entity_list:
                await _add_entity(buffer_list, entity)
            enemies.append( buffer_list )

    else:
        for entity in room_instance.enemies:
            await _add_entity(enemies, entity)


    return enemies


async def _add_entity(list_to_append: list[MobModel], entity: BaseEntityGS):
    mob_model = MobModel(
        name=entity.name,
        desc=entity.description,

        lvl=entity.lvl,

        hp=randint(entity.min_hp, entity.max_hp),
        mana=randint(entity.min_mana, entity.max_mana),

        actions=entity.actions,
        actions_max=entity.actions_max,
        bonus_actions=entity.bonus_actions,
        bonus_actions_max=entity.bonus_actions_max,

        stat_strength=entity.stat_strength,
        stat_dexterity=entity.stat_dexterity,
        stat_constitution=entity.stat_constitution,
        stat_intelligence=entity.stat_intelligence,
        stat_will=entity.stat_will,

    )

    mob_model.scripts = [
        "script/enemy/remove_db",
    ]

    list_to_append.append( mob_model )





async def _update_room_model(room_model: RoomModel, room_schema: RoomMeshSchema):
    for attr, value in room_schema.model_dump().items():
        if not hasattr(room_model, attr):
            continue
        setattr(room_model, attr, value)

    room_model.text_pointer = 1

    room_model.stoppers = []
    room_model.updated_states = {}

    room_model.enemies = []
    room_model.loot = []

    room_model.can_exit = False



async def _update_room_model_by_file(room_model: RoomModel) -> RoomGS:
    cls_name: str = await importer.get_first_cls_name(
        file_path=room_model.room_path,
    )
    room_cls: type[RoomGS] = await importer.import_class(
        abs_path=room_model.room_path,
        class_name=cls_name,
    )
    room_instance = room_cls()

    room_model.texts = room_instance.texts
    room_model.state = room_instance.entry_state


    return room_instance