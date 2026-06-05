from game_data.templates.effect import BaseEffect, StatModifierEffect
from game_data import const

class StrengthModifierEffect( StatModifierEffect ):
    id = "strength"
    updatable = False
    alignment = BaseEffect.Alignment.NEGATIVE

    @staticmethod
    def get_stats_modifiers(
            value_1: int,
            value_2: int,
            value_3: int,
            value_4: int,
    ) -> dict[str, int]:
        return {const.Stat.Strength: value_1}