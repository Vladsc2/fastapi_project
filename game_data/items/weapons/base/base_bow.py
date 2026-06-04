from game_data.templates.items import WeaponItem
from game_data.templates.damage_formula import DamageFormula
from game_data import const

class BaseBow( WeaponItem ):

    id = "base_bow"

    name = "Базовый лук"
    desc = "Базовый лук, используемый для тестов"

    slot = const.WeaponConst.Slot.RANGE

    costs = {
        const.Cost.BONUS_ACTION: 1,
    }

    damages = [
        DamageFormula(
            damage_type=const.DamageType.Weapon.PIERCING,
            dice={
                const.Roll.ROLL_4: 1,
            },
            min_damage=2,
        )
    ]

    modifiers = [ const.Stat.Dexterity ]

