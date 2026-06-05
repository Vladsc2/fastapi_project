from game_data import const
from game_data.const import const_modifier
from game_data.templates.damage_formula import DamageFormula
from game_data.templates.effect import EffectApplication


class BaseItem():
    _category: str = "item"
    id: str

    name: str = "Item"
    desc: str = ""

    sell_price: int = 1
    buy_price: int = 5

    can_be_sold: bool = True




class JunkItem(BaseItem):
    _category = BaseItem._category + "/junk"


class CoinItem(BaseItem):
    _category = BaseItem._category + "/coin"
    can_be_sold = False


class WeaponItem(BaseItem):
    _category = BaseItem._category + "/weapon"

    slot: str

    costs: dict[str, int]

    damages: list[DamageFormula]

    # Модификатор - const.Stat, что использовать во время атаки на попадание и для бонуса
    modifiers: list[str] = []

    # EffectApplication - описание, какой эффект и на сколько наложить при атаке
    effects: list[EffectApplication] = []




class ArmorItem( BaseItem ):
    _category = BaseItem._category + "/armor"

    armor_class: int



class EquipmentItem( BaseItem ):
    _category = BaseItem._category + "/eq"
    equipment_slot: str



class UsableItem(BaseItem):
    _category = BaseItem._category + "/usable"

    cost: dict[str, int]
    effects: list = []




def get_str_damage_formula(weapon: WeaponItem) -> str:
    text = ""
    damage_formula: DamageFormula
    for damage_formula in weapon.damages:
        text += f"[ {const_modifier.get_readable_damage_type(damage_formula.damage_type)} "

        buffer_text = ""
        for dice_type, dice_count in damage_formula.dice.items():
            if buffer_text != "":
                buffer_text += " + "
            readable_dice_type = const_modifier.get_readable_dice_name( dice_type )
            buffer_text += f"{dice_count}{readable_dice_type}"
        text += buffer_text

        if damage_formula.min_damage > 0:
            text += f", >{damage_formula.min_damage}"

        if damage_formula.max_damage > 0:
            text += f", <{damage_formula.max_damage}"

        text += " ] "

    return text