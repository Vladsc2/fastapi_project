from app.models.game import GameModel
from game_data.templates.damage_formula import DamageFormula, Damage
from game_data.templates.items import WeaponItem
from game_data.const import const_modifier
from game_data import const

from app.game_systems.roll import get_roll_dict


async def get_roll_dict_if_matches_formulas(
        game_model: GameModel,
        damage_list: list[DamageFormula]
) -> dict[str, list[int]] | None:

    roll_dict = await get_roll_dict(game_model)

    all_damage_dice: dict[str, int] = {}

    for damage in damage_list:
        for dice_type, dice_count in damage.dice.items():
            saved_count = all_damage_dice.get(dice_type, 0)
            all_damage_dice[dice_type] = saved_count + dice_count


    for dice_type, dice_count in all_damage_dice.items():
        dice_list = roll_dict.get( dice_type )
        if len(dice_list) < dice_count:
            return None

    return roll_dict



async def get_damage_from_formula(
        roll_dict: dict[str, list[int]],
        damage_formula: DamageFormula,
) -> tuple[str, Damage]:
    text = "  Формирование урона:\n"
    dice_count = 0
    damage_values = []

    for dice_type, dice_count in damage_formula.dice.items():
        roll_list = roll_dict.get(dice_type)
        text += f"    Кубик {const_modifier.get_readable_dice_name(dice_type)} | "

        for i in range(dice_count):
            roll_value = roll_list.pop(0)
            damage_values.append( roll_value )
            if i == 0:
                text += f"{roll_value}"
            else:
                text += f" + {roll_value}"
            dice_count += 1


    damage_value = sum(damage_values)
    if dice_count > 1:
        text += f" = {damage_value}"
    text += "\n"

    if damage_formula.min_damage > 0 and damage_value < damage_formula.min_damage:
        damage_value = damage_formula.min_damage
        text += f"    Приведено к минимальному урону: {damage_value}\n"
    if damage_formula.max_damage > 0 and damage_value > damage_formula.max_damage:
        damage_value = damage_formula.max_damage
        text += f"    Приведено к максимальному урону: {damage_value}\n"

    return text, Damage(damage_type=damage_formula.damage_type, value=damage_value)

