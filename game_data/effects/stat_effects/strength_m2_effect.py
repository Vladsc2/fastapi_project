from game_data.templates.effect import BaseEffect, StatModifierEffect
from game_data import const

class StrengthM2Effect( StatModifierEffect ):
    id = "strength-m2"
    event = const.Event.END_TURN
    updatable = False
    alignment = BaseEffect.Alignment.NEGATIVE

    stats = {
        const.Stat.Strength: -2,
    }