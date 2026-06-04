from dataclasses import dataclass, field
from game_data import const

@dataclass
class DamageFormula():
    damage_type: str = const.DamageType.Weapon.SLASHING

    # dict[const.Roll, count]
    dice: dict = field(default_factory=dict)

    # 0 is unused
    min_damage: int = 0
    max_damage: int = 0



@dataclass
class Damage():
    damage_type: str
    value: int