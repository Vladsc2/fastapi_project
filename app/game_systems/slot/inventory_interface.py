from app.schemas.slot import ItemSlot
from app.models.game import MainCharacterModel, InventoryModel

"""
    Interfaces
"""


async def pick_up_item(character: MainCharacterModel, item_url: str) -> str:
    pass



async def remove_item(character: MainCharacterModel, item_url: str) -> str:
    pass



async def view_item(character: MainCharacterModel, item_url: str) -> str:
    pass


"""
    Realization
"""

