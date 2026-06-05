from game_data.templates.effect import BaseEffect, StatModifierEffect
from game_data import const

class ConstitutionModifierEffect( StatModifierEffect ):
    id = "constitution"
    updatable = True
    alignment = BaseEffect.Alignment.NEGATIVE

    def get_stats_modifiers(
            self,
            value_1: int,
            value_2: int,
            value_3: int,
            value_4: int,
    ) -> dict[str, int]:
        return {const.Stat.Constitution: value_1}