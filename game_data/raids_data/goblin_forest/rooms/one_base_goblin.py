from game_data.templates.room import BattleRoom
from game_data.raids_data.goblin_forest.entities import BaseGoblin
from dataclasses import dataclass, field

@dataclass
class OneBaseGoblinRoom( BattleRoom ):
    name = "Поляна под солнцем"

    texts: list[str] = field(default_factory=lambda: [
        """
            Вы входите на поляну, и видите на ней одинокого гоблина.
            
            Он замечает вас и готовится к битве
        """
    ])


    enemies: list = field(default_factory=lambda: [BaseGoblin])