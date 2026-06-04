from game_data.templates.items import WeaponItem
from game_data.templates.damage_formula import DamageFormula
from game_data import const

class BaseFists( WeaponItem ):

    id = "base_fists"

    name = "Кулаки"
    desc = "Используется, когда в слоте оружия ближнего боя не установлено оружие"

    slot = const.WeaponConst.Slot.CLOSE

    costs = {
        const.Cost.ACTION: 1,
    }

    damages = [
        DamageFormula(
            damage_type=const.DamageType.Weapon.BLUDGEONING,
            dice={const.Roll.ROLL_4: 1},
        )
    ]

    modifiers = [ const.Stat.Strength ]