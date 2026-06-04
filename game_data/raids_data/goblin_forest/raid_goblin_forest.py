from game_data.templates.raid import AbstractRaidGS
import os
from dataclasses import dataclass

@dataclass
class RaidGoblinForestGS( AbstractRaidGS ):

    name = "Лес гоблинов"
    description = "Лес где обитают гоблины, воюющие с империей"

    min_lines = 5
    max_lines = 8

    min_rooms = 1
    max_rooms = 4


    room_loot_min_percent = 5
    room_loot_max_percent = 10

    room_battle_loot_min_percent = 10
    room_battle_loot_max_percent = 30

    room_treasure_min_percent = 0
    room_treasure_max_percent = 5

    room_skill_check_min_percent = 10
    room_skill_check_max_percent = 40
    room_skill_check_mode_percent = 20

    raid_dir = os.path.dirname( __file__ )

