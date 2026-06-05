from game_data.templates.items import WeaponItem
from game_data.templates.damage_formula import DamageFormula
from game_data.templates.effect import EffectApplication
from game_data import const

class BaseSword( WeaponItem ):

    id = "weakened_immune_bow"

    name = "Лук ослабления иммунитета"
    desc = "При атаке снимает с цели 4 телосложения"

    slot = const.WeaponConst.Slot.RANGE

    costs = {
        const.Cost.BONUS_ACTION: 0,
    }

    damages = [
        DamageFormula(
            damage_type=const.DamageType.Weapon.PIERCING,
            dice={
                const.Roll.ROLL_8: 1,
            },
            min_damage=3,
        )
    ]

    modifiers = [ const.Stat.Dexterity ]

    effects = [ EffectApplication(
        url="effect/stat/constitution",
        time=4,
        value_1=-4,
    ) ]