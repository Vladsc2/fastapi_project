from game_data.templates.items import WeaponItem
from game_data.templates.damage_formula import DamageFormula
from game_data import const

class GodKiller( WeaponItem ):

    id = "god_killer"

    name = "Убийца богов"
    desc = "Меч, обладающей невероятной мощью"

    slot = const.WeaponConst.Slot.CLOSE

    costs = {}

    damages = [
        DamageFormula(
            damage_type=const.DamageType.Exotic.FORCE,
            dice={
                const.Roll.ROLL_20: 1,
            },
            min_damage=100,
        )
    ]

    modifiers = [ const.Stat.Strength ]

