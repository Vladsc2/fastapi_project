from game_data.templates.effect import BaseEffect
import game_data.effects.tick_effects
import game_data.effects.stat_effects

_effects = {}


def _register_all_effects():

    for base_subclass in BaseEffect.__subclasses__():

        for cls in base_subclass.__subclasses__():

            _effects[ cls._category + "/" + cls.id ] = cls



def get_effect_by_url(
        url: str,
) -> type[BaseEffect] | None:

    return _effects.get( url, None )



_register_all_effects()
