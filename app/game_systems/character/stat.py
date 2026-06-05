from app.models.game import BaseCharacterModel
from app.schemas.effect import EffectSchema
from game_data import const
from game_data.templates.effect import BaseEffect, StatModifierEffect
from game_data.effects import effect_system

def get_stat_modifier(
        entity_model: BaseCharacterModel,
        stat: str,
) -> int:

    stat_value = 0
    if stat == const.Stat.Strength:
        stat_value = entity_model.stat_strength
    elif stat == const.Stat.Dexterity:
        stat_value = entity_model.stat_dexterity
    elif stat == const.Stat.Constitution:
        stat_value = entity_model.stat_constitution
    elif stat == const.Stat.Intelligence:
        stat_value = entity_model.stat_intelligence
    elif stat == const.Stat.Will:
        stat_value = entity_model.stat_will


    stat_value = _update_stat_value_from_effects(entity_model, stat_value, stat)

    modifier = _calc_modifier( stat_value )

    return modifier



def _update_stat_value_from_effects(
        entity_model: BaseCharacterModel,
        stat_value: int,
        stat: str,
) -> int:

    for effect_dict in entity_model.effects:
        effect_schema = EffectSchema( **effect_dict )

        if effect_schema.effect_type != BaseEffect.Type.STAT_MODIFIER:
            continue

        effect: StatModifierEffect = effect_system.get_effect_by_url(effect_schema.effect_url)
        stat_dict = effect.get_stats_modifiers(
            value_1=effect_schema.value_1,
            value_2=effect_schema.value_2,
            value_3=effect_schema.value_3,
            value_4=effect_schema.value_4
        )
        for stat_const, stat_modifier in stat_dict.items():
            if stat != stat_const:
                continue
            stat_value += stat_modifier

    return stat_value



def _calc_modifier(
        state_value: int,
) -> int:
    if state_value == 20:
        # Обработка нечетности, 19 = 6, 20 = 7
        return 7

    state_value = state_value - 7

    modifier = int( state_value / 2 )

    return modifier