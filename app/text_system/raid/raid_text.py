from app.models.raid import RaidModel
from app.models.room import RoomModel
from app.schemas.room import RoomMeshSchema
from game_data.raids_data.goblin_forest import RaidGoblinForestGS


def get_raid_mesh_text(
        raid_model: RaidModel,
        mesh: list[list[RoomMeshSchema]],
) -> str:
    string = f"""
        Рейд: {raid_model.name}
        Описание: {raid_model.desc}
        
"""

    for index, line in enumerate(mesh):
        line_string = f"line {index+1}"
        if index+1 == raid_model.current_line:
            line_string += "  <<<"
        line_string += "\n"

        for room in line:
            if room.name == "":
                line_string += f"   Room={room.room_type}"
            else:
                line_string += f"   {room.name}"

            if room is not line[-1]:
                line_string += ", "
            else:
                line_string += "\n"

        string += line_string


    return string




def get_raid_state_text(
        raid_model: RaidModel,
        rooms: list[RoomMeshSchema],
) -> str:

    string = ""

    if raid_model.name == RaidGoblinForestGS.name:
        string += _get_goblin_forest_text()

    for index, room in enumerate(rooms):
        if room.name == "":
            string += f' {index+1}) <a href="/raid/select-{index+1}">Локация {room.room_type}</a>\n'
        else:
            string += f' {index+1}) <a href="/raid/select-{index+1}">{room.name}</a>\n'

    return string



def _get_goblin_forest_text():
    return """
        Вы идете дальше по лесу, и видите несколько возможных путей
        
"""

