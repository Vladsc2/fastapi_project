from game_data.templates.script import BaseScript
import game_data.scripts.enemy_scripts
import game_data.scripts.player_scripts
import game_data.scripts.system_scripts

_scripts = {}


def _register_all_scripts():

    for base_subclass in BaseScript.__subclasses__():

        for cls in base_subclass.__subclasses__():

            _scripts[ cls._category + "/" + cls.id ] = cls



def get_script_by_url(
        url: str,
) -> type[BaseScript] | None:

    return _scripts.get( url, None )



_register_all_scripts()
