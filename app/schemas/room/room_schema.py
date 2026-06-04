from app.schemas.base import BaseSchema
from game_data import const

class RoomMeshSchema( BaseSchema ):

    room_type: str = const.RoomTypes.BATTLE
    room_path: str = ""

    name: str = ""

