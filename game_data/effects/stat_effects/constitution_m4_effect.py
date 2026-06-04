from game_data.templates.effect import BaseEffect, StatModifierEffect
from game_data import const

class ConstitutionM4U( StatModifierEffect ):
    id = "constitution-m4-u"
    event = const.Event.END_TURN
    updatable = True
    alignment = BaseEffect.Alignment.NEGATIVE

    stats = {
        const.Stat.Constitution: -4,
    }