from dataclasses import dataclass, field
from game_data import const


@dataclass
class RoomGS():
    # system
    room_type: str = const.RoomTypes.BATTLE
    entry_state: str = const.RoomStates.General.TEXT

    # override
    name: str = "Неизвестное место"

    texts: list = field(default_factory=list)

    enemies: list = field(default_factory=list)
    loot: list = field(default_factory=list)



    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(room_type={self.room_type})"



class BattleRoom( RoomGS ):
    room_type = const.RoomTypes.BATTLE


class LootRoom( RoomGS ):
    room_type = const.RoomTypes.LOOT