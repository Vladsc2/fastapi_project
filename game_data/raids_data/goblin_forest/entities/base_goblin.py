from game_data.templates.entity import BaseEntityGS
from dataclasses import dataclass

@dataclass
class BaseGoblin( BaseEntityGS ):

    name = "Base Goblin"

    min_hp = 6
    max_hp = 9

    weapon_id = 1