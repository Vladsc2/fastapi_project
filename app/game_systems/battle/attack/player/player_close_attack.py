from fastapi import HTTPException, status

from app.models.game import GameModel
from app.models.room import RoomModel
from app.models.game import MobModel
from game_data.templates.items import WeaponItem
from game_data.templates.damage_formula import Damage

from game_data import const
from game_data.const import const_modifier

from app.game_systems.battle.attack.player import player_attack_validator
from app.game_systems.battle.attack.player import player_attack_text
from app.game_systems.battle.attack.abstract import abstract_attack

from app.game_systems.room.tools import stopper_checker
from app.game_systems.roll import clear_roll, clear_all_rolls, get_roll
from game_data.items import items_system
from app.game_systems.damage import damage_module

"""
    Interfaces
"""

async def get_available_targets(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
        weapon: WeaponItem,
) -> str:

    if (stopper_checker.check_stopper(room_model, None)
            or stopper_checker.check_stopper(room_model, const.Stopper.Battle.AWAIT_TARGET_CLOSE_ATTACK)):
        return await _to_select_enemy(
            game_model=game_model,
            room_model=room_model,
            enemies=enemies,
            weapon=weapon,
        )


    return (f"Не удалось обработать событие, во время работы с атакой ближнего боя\n\n"
            f"  {__file__}\n\n"
            f"  - state: {room_model.state}\n"
            f"  - stoppers: {room_model.stoppers}\n")



async def close_attack(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
        weapon: WeaponItem,
        target: int | None = None
) -> str:

    if stopper_checker.check_stopper(room_model, const.Stopper.Battle.AWAIT_TARGET_CLOSE_ATTACK):
        return await _select_target(
            game_model=game_model,
            room_model=room_model,
            enemies=enemies,
            target=target,
            weapon=weapon,
        )


    elif stopper_checker.check_stopper(room_model, [
        const.Stopper.Battle.AWAIT_HIT_ROLL_CLOSE_ATTACK,
        const.Stopper.ENEMY_POINTERS,
    ]):
        return await _hitting_roll_awaiting(
            game_model=game_model,
            room_model=room_model,
            enemies=enemies,
            weapon=weapon,
        )


    elif stopper_checker.check_stopper(room_model, [
        const.Stopper.Battle.AWAIT_DAMAGE_ROLL_CLOSE_ATTACK,
        const.Stopper.ENEMY_POINTERS,
    ]):
        return await _damage_roll_awaiting(
            game_model=game_model,
            room_model=room_model,
            enemies=enemies,
            weapon=weapon,
        )


    return (f"Не удалось обработать событие, во время выбора цели для атаки ближнего боя\n\n"
            f"  {__file__}\n\n"
            f"  - state: {room_model.state}\n"
            f"  - stoppers: {room_model.stoppers}\n")



"""
    Realization
"""

async def _to_select_enemy(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
        weapon: WeaponItem,
) -> str:
    check_string: str | None = await player_attack_validator.check_cost(
        char=game_model.character,
        weapon=weapon
    )
    if check_string is not None:
        return check_string

    text = f"Выберите цель для атаки\n\n"

    for index, mob_model in enumerate(enemies):
        text += f" {index+1}) "
        text += f"<a href='/room/close_attack-{index+1}'>{mob_model.name}</a>"
        text += f" (lvl={mob_model.lvl}, hp={mob_model.hp}, mana={mob_model.mana})\n\n"

    text += f"<a href='/room'>Назад</a>"

    room_model.stoppers = [const.Stopper.Battle.AWAIT_TARGET_CLOSE_ATTACK]

    return text



async def _select_target(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
        target: int,
        weapon: WeaponItem,
) -> str:

    if target < 1 or target > len(enemies):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"""
                    Недопустимый номер цели. 
                        - Переданный номер: {target}
                        - Минимальный номер: 1
                        - Максимальный номер: {len(enemies) + 1}
            """
        )

    room_model.stoppers = [
        const.Stopper.Battle.AWAIT_HIT_ROLL_CLOSE_ATTACK,
        const_modifier.target_number_to_target_const( target_number=target )
    ]

    enemy = enemies[target-1]

    text = player_attack_text.request_hitting_target_roll(enemy, 'close_attack')

    await clear_roll(game_model, const.Roll.ROLL_20)

    return text



async def _hitting_roll_awaiting(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
        weapon: WeaponItem,
) -> str:
    const_pointer = stopper_checker.get_stopper_in_list(
        room_model,
        const.Stopper.ENEMY_POINTERS,
    )
    enemy = enemies[ const_modifier.target_const_to_target_number( const_pointer )-1 ]


    roll_value: int | None = await get_roll(game_model, const.Roll.ROLL_20)
    if roll_value is None:
        return player_attack_text.request_hitting_target_roll(enemy, 'close_attack')

    armor = items_system.get_item_by_url( enemy.armor_url )

    is_hit, text = await abstract_attack.attack_hit(
        attacker=game_model.character,
        target=enemy,
        roll_value=roll_value,
        armor=armor,
        weapon=weapon
    )

    if not is_hit:
        room_model.stoppers = []
        text += " <a href='/room'>Далее</a>"
        return text

    room_model.stoppers = [
        const.Stopper.Battle.AWAIT_DAMAGE_ROLL_CLOSE_ATTACK,
        const_pointer,
    ]

    await clear_all_rolls(game_model)

    text += player_attack_text.request_damage_text(weapon)

    text += " <a href='/room/close_attack-1'>Далее</a>"

    return text



async def _damage_roll_awaiting(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
        weapon: WeaponItem,
) -> str:

    const_pointer = stopper_checker.get_stopper_in_list(
        room_model,
        const.Stopper.ENEMY_POINTERS,
    )
    enemy = enemies[ const_modifier.target_const_to_target_number( const_pointer )-1 ]


    roll_dict: dict[str, list[int]] = await damage_module.get_roll_dict_if_matches_formulas(
        game_model=game_model,
        damage_list=weapon.damages
    )
    if roll_dict is None:
        text = player_attack_text.request_damage_text(weapon)
        text += " <a href='/room/close_attack-1'>Далее</a>"
        return text

    text = await abstract_attack.attack_damage(
        game_model=game_model,
        attacker=game_model.character,
        target=enemy,
        weapon=weapon,
        roll_dict=roll_dict,
    )

    room_model.stoppers = []

    text += " <a href='/room'>Далее</a>"

    return text