from game_data.templates.items import WeaponItem
from game_data.templates.damage_formula import DamageFormula
from game_data.templates.effect import EffectApplication
from game_data import const

class GodKiller( WeaponItem ):

    id = "poison_dagger"

    name = "Отравленный кинжал"
    desc = "Кинжал, накладывающий эффект отравления на цель"

    slot = const.WeaponConst.Slot.CLOSE

    costs = {
        const.Cost.ACTION: 0,
    }

    damages = [
        DamageFormula(
            damage_type=const.DamageType.Weapon.PIERCING,
            dice={
                const.Roll.ROLL_4: 1,
            },
        )
    ]

    modifiers = [ const.Stat.Strength, const.Stat.Dexterity ]

    effects = [ EffectApplication(url="effect/tick/poison", time=3) ]