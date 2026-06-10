from app.models import GameModel
from app.models.game import BaseCharacterModel, MainCharacterModel, MobModel
from game_data.templates.items import WeaponItem, ArmorItem

from game_data import const
from game_data.const import const_modifier

from app.game_systems.character.stat import get_stat_modifier
from app.game_systems.character import points
from app.game_systems.damage import damage_module
from app.game_systems.character import entity_health
from app.game_systems.character import entity_effects

"""
    Interface
"""

async def attack_hit(
        attacker: BaseCharacterModel,
        target: BaseCharacterModel,
        roll_value: int,
        armor: ArmorItem | None,
        weapon: WeaponItem,
) -> tuple[bool, str]:
    await points.write_off_cost(
        char=attacker,
        costs=weapon.costs
    )

    text = f"{attacker.name} атакует {target.name}\n\n"

    text += f"  Формирования значения попадания:\n"
    text += f"    Значение d20 на попадание - {roll_value}\n"

    add_text, modifier = await _get_weapon_modifier(attacker, weapon)
    text += add_text

    hit_value = roll_value + modifier

    if armor is None:
        armor_class = 10
    else:
        armor_class = armor.armor_class

    if hit_value < armor_class:
        text += f"    Попадание {hit_value} < Класс брони {armor_class}\n"
        text += f"    Промах!\n\n"
        return False, text


    text += f"    Попадание {hit_value} >= Класс брони {armor_class}\n"
    text += f"    Попадание!\n\n"

    return True, text



async def attack_damage(
        game_model: GameModel,
        attacker: BaseCharacterModel,
        target: BaseCharacterModel,
        weapon: WeaponItem,
        roll_dict: dict[str, list[int]],
        enemies: list[MobModel]
) -> str:
    text = ""

    for damage_formula in weapon.damages:
        additional_text, damage = await damage_module.get_damage_from_formula(roll_dict, damage_formula)
        text += additional_text

        additional_text, modifier = await _get_weapon_modifier(attacker, weapon)
        text += additional_text

        damage.value += modifier

        text += await entity_health.entity_take_damage(
            game_model=game_model,
            attacker=attacker,
            target=target,
            damage=damage,
            enemies=enemies,
        )

    if target.hp > 0:
        for effect_app in weapon.effects:
            caster_id = None if isinstance(attacker, MainCharacterModel) else attacker.id
            text += await entity_effects.add_effect(target, caster_id, effect_app)


    return text





"""
    Realization
"""

async def _get_weapon_modifier(
        attacker: BaseCharacterModel,
        weapon: WeaponItem,
) -> tuple[str, int]:

    if len(weapon.modifiers) == 0:
        return "", 0

    text = ""

    if len(weapon.modifiers) == 1:
        modifier_type = weapon.modifiers[0]
        modifier = get_stat_modifier(attacker, modifier_type)
        text += (f"    Модификатор оружия - {const_modifier.get_readable_stat(modifier_type)}\n"
                 f"    Модификатор персонажа - {modifier}\n")

    else:
        modifier = -9999
        modifier_type = const.NONE_CONST
        for iter_modifier_type in weapon.modifiers:
            modifier_value = get_stat_modifier(attacker, iter_modifier_type)
            if modifier_value > modifier:
                modifier = modifier_value
                modifier_type = iter_modifier_type

        text += (f"    Модификаторы оружия - {[const_modifier.get_readable_stat(m) for m in weapon.modifiers]}\n"
                 f"    Наибольший модификатор персонажа - "
                 f" {const_modifier.get_readable_stat(modifier_type)}&{modifier}\n")


    return text, modifier
