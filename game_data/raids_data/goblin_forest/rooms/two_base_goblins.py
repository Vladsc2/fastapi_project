from game_data.templates.room import BattleRoom
from game_data.raids_data.goblin_forest.entities import BaseGoblin
from dataclasses import dataclass, field

@dataclass
class TwoBaseGoblinRoom( BattleRoom ):
    name = "Густой лес"

    texts: list[str] = field(default_factory=lambda: [
        """
            Вы бродите по густому лесу, и встречаете двух гоблинов
            
            Вы пытаетесь спрятаться, но они вас замечают
        """
    ])

    enemies: list = field(default_factory=lambda: [BaseGoblin, BaseGoblin])