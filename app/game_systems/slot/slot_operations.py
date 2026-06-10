from app.schemas.slot import ItemSlot
from app.models.game import MainCharacterModel, InventoryModel

"""
    Interfaces
"""

async def add_slot_to_slot_list(slot_list: list[ItemSlot], slot: ItemSlot, slot_limit: int = -1) -> bool:
    """
        Возвращает True если предметы из слота удалось добавить в список слотов
        Возвращает False, если в слоте остались предметы, не добавленные в список
    """
    return await _add_slot_to_slot_list(slot_list, slot, slot_limit)





"""
    Realization
"""

async def _add_slot_to_slot_list(slot_list: list[ItemSlot], slot: ItemSlot, slot_limit: int) -> bool:
    if slot.count == 0:
        return True

    # Максимально добавляем предметы в слоты
    for inside_slot in slot_list:

        if inside_slot.url != slot.url:
            continue

        max_add_value = inside_slot.stack_limit - inside_slot.count

        if max_add_value >= slot.count:
            inside_slot.count += slot.count
            slot.count = 0
            return True
        else:
            slot.count -= max_add_value
            inside_slot.count += max_add_value


    # Если осталось содержимое в слоте, пытаемся создать новый
    if slot_limit != -1 and len(slot_list) >= slot_limit:
        return False

    slot_list.append(
        ItemSlot(
            url=slot.url,
            name=slot.name,
            count=slot.count,
            stack_limit=slot.stack_limit,
        )
    )
    slot.count = 0

    return True