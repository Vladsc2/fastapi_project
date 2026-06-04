from app.models.game import MobModel

from game_data.const import const_modifier

from game_data.templates.items import WeaponItem, ArmorItem, get_str_damage_formula
from game_data.templates.damage_formula import DamageFormula

from game_data.items import items_system

from game_data import const


def request_hitting_target_roll(
        enemy: MobModel,
        next_url: str,
) -> str:
    enemy_armor: ArmorItem | None = items_system.get_item_by_url( enemy.armor_url )

    text = f"Выбранная цель: {enemy.name}  [hp = {enemy.hp}, mana = {enemy.mana}]\n\n"
    if enemy_armor is None:
        text += f"  Класс брони цели: 10\n\n"
    else:
        text += f"  Класс брони цели: {enemy_armor.armor_class}\n\n"
    text += f"  Кидайте на попадание\n\n"

    text += f" <a href='/room/{next_url}-1'>Далее</a>"

    return text



def request_damage_text(
        weapon: WeaponItem,
) -> str:
    if weapon.slot == const.WeaponConst.Slot.CLOSE:
        text = f"  Оружие ближнего боя: {weapon.name}\n\n"
    else:
        text = f"  Оружие дальнего боя: {weapon.name}\n\n"

    text += f"    Формула урона: {get_str_damage_formula(weapon)}\n\n"

    text += _get_roll_damage_text(weapon)

    return text



def get_no_range_weapon_text() -> str:
    return (f"У вас не экипировано оружия дальнего боя\n\n"
            f" <a href='/room'>Назад</a>")



def _get_roll_damage_text(
        weapon: WeaponItem,
) -> str:
    text = "  Кидайте на урон"
    for damage_formula in weapon.damages:
        for dice_type, dice_count in damage_formula.dice.items():
            text += f" {dice_count}{const_modifier.get_readable_dice_name(dice_type)}"
    text += "\n\n"

    return text