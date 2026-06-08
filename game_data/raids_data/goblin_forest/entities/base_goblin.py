from game_data.templates.entity import BaseEntityGS, DropSpec
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


    exp = 1
    loot: list = field(default_factory=[
        DropSpec(
            url="item/junk/board",
            quantity=1,
            chance=35,
        ),
        DropSpec(
            url="item/junk/broken_arrow",
            quantity=2,
            chance=20,
            single_mode=True,
        ),
        DropSpec(
            url="item/junk/broken_arrow",
            quantity=1,
            chance=15,
        ),
        DropSpec(
            url="item/coin/copper",
            quantity=10,
            chance=25,
        )
    ])