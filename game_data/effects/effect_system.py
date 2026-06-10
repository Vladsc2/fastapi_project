from game_data.templates.effect import BaseEffect
import game_data.effects.tick_effects
import game_data.effects.stat_effects

from app.models.game import GameModel, MobModel, BaseCharacterModel
from app.schemas.effect import EffectSchema

_effects = {}


def _register_all_effects():

    for base_subclass in BaseEffect.__subclasses__():

        for cls in base_subclass.__subclasses__():

            _effects[ cls._category + "/" + cls.id ] = cls



def get_effect_by_url(
        url: str,
) -> type[BaseEffect] | None:

    return _effects.get( url, None )



def get_effect_instance(
        url: str,
        caster: BaseCharacterModel,
        target: BaseCharacterModel,
        game_model: GameModel,
        effect_schema: EffectSchema,
        enemies: list[MobModel],
) -> BaseEffect | None:
    effect_cls = _effects.get( url, None )
    if effect_cls is None:
        return None
    return _form_effect_instance(
        effect_cls=effect_cls,
        caster=caster,
        target=target,
        enemies=enemies,
        game_model=game_model,
        effect_schema=effect_schema,
    )


def _form_effect_instance(
        effect_cls: type[BaseEffect],
        caster: BaseCharacterModel,
        target: BaseCharacterModel,
        game_model: GameModel,
        effect_schema: EffectSchema,
        enemies: list[MobModel]
) -> BaseEffect:
    effect = effect_cls()
    effect._form_effect_meta(
        game_model=game_model,
        room_model=game_model.room,
        player_char=game_model.character,
        caster=caster,
        target=target,
        enemies=enemies,

        value_1=effect_schema.value_1,
        value_2=effect_schema.value_2,
        value_3=effect_schema.value_3,
        value_4=effect_schema.value_4,
    )
    return effect



_register_all_effects()
