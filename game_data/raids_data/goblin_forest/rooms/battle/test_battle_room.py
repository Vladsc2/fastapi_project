from game_data.templates.room import BattleRoom
from game_data.raids_data.goblin_forest.entities import BaseGoblin as Enemy
from dataclasses import dataclass, field

@dataclass
class OneBaseGoblinRoom( BattleRoom ):
    name = "Тестовая комната битвы"

    texts: list = field(default_factory=lambda: [
        [
            "Текст 1"
        ],
        [
            "Текст 2"
        ]
    ] )

    enemies: list = field(default_factory=lambda: [
        [
            Enemy
        ],
        [
            Enemy
        ],
        [
            Enemy
        ],
        [
            Enemy
        ]
    ])