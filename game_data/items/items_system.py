from game_data.templates.items import BaseItem
import game_data.items.equipments
import game_data.items.junk
import game_data.items.usable
import game_data.items.weapons

_items = {}


def _register_all_items():

    for base_subclass in BaseItem.__subclasses__():

        for cls in base_subclass.__subclasses__():

            _items[ cls._category + "/" + cls.id ] = cls



def get_item_by_url(
        url: str,
) -> BaseItem | None:

    return _items.get( url, None )



_register_all_items()
