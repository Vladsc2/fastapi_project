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