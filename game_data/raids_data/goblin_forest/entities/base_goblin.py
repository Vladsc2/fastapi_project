from game_data.templates.entity import BaseEntityGS
from game_data.templates.effect import EffectApplication
from dataclasses import dataclass, field

@dataclass
class BaseGoblin( BaseEntityGS ):

    name = "Base Goblin"

    min_hp = 6
    max_hp = 9

    effects: list = field(default_factory=lambda: [
        EffectApplication(
            url="effect/tick/poison",
            time=5,
            ignore_save_throw=True
        )
    ])