from dataclasses import dataclass, field

@dataclass
class AbstractRaidGS():

    name: str = "Raid"
    description: str = ""

    min_lines: int = 1
    max_lines: int = 1
    mode_lines: int = 0

    min_rooms: int = 1
    max_rooms: int = 4
    mode_rooms: int = 2.5


    # Процент заполнения рейда, а не шанс выпадения
    # battle_room это базовая, которой заполняется рейд

    room_loot_min_percent: float = 0
    room_loot_max_percent: float = 0
    room_loot_mode_percent: float = 0

    room_battle_loot_min_percent: float = 0
    room_battle_loot_max_percent: float = 0
    room_battle_loot_mode_percent: float = 0

    room_treasure_min_percent: float = 0
    room_treasure_max_percent: float = 0
    room_treasure_mode_percent: float = 0

    room_skill_check_min_percent: float = 0
    room_skill_check_max_percent: float = 0
    room_skill_check_mode_percent: float = 0


    raid_dir: str = ""