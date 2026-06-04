from game_data.templates.items import WeaponItem
from game_data.templates.damage_formula import DamageFormula
from game_data import const

class GoblinSword( WeaponItem ):

    id = "goblin_sword_1"

    name = "Гоблинский меч"

    slot = const.WeaponConst.Slot.CLOSE
    costs = {
        const.Cost.ACTION: 1,
    }

    damages = [
        DamageFormula(
            dice={const.Roll.ROLL_6: 1}
        )
    ]

    modifiers = [ const.Stat.Strength ]