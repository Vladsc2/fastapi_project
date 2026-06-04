from game_data.templates.items import WeaponItem
from game_data.templates.damage_formula import DamageFormula
from game_data import const

class BaseSword( WeaponItem ):

    id = "Базовый меч"

    name = "Базовый меч"
    desc = "Самый обычный меч. Тестовый предмет. Никаких особенностей"

    slot = const.WeaponConst.Slot.CLOSE

    costs = {
        const.Cost.ACTION: 1,
    }

    damages = [
        DamageFormula(
            damage_type=const.DamageType.Weapon.SLASHING,
            dice={
                const.Roll.ROLL_4: 2,
            },
            min_damage=4,
        )
    ]

    modifiers = [ const.Stat.Strength ]