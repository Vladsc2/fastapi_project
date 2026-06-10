from app.models.game import GameModel
from app.models.room import RoomModel
from app.models.game import MobModel
from game_data.templates.items import WeaponItem
from game_data import const

from app.game_systems.room.tools import state_manager

from app.game_systems.room.room_actions import room_text_action
from app.game_systems.battle.battle_starter import battle_starter
from app.game_systems.battle.battle_system import enemies_turn
from app.game_systems.battle.battle_system import player_turn
from app.game_systems.battle.attack.player import player_close_attack
from app.game_systems.battle.attack.player import player_range_attack
from app.game_systems.battle.loot_enemies import loot_enemies
from app.game_systems.room.leave import leave_room

from app.game_systems.character import entity_script

"""
    Interfaces
"""

async def home_room_handle(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
) -> str:
    string = await _home_room_handle(game_model, room_model, enemies)

    return string


async def end_player_turn(game_model: GameModel, enemies: list[MobModel]) -> str:
    string = await player_turn.end_player_turn(game_model, enemies)

    return string



async def close_attack_to_select_target(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
        weapon: WeaponItem,     # check cost
) -> str:
    return await player_close_attack.get_available_targets(
        game_model=game_model,
        room_model=game_model.room,
        enemies=enemies,
        weapon=weapon,
    )



async def close_attack(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
        weapon: WeaponItem,
        target: int | None,
) -> str:
    return await player_close_attack.close_attack(
        game_model=game_model,
        room_model=game_model.room,
        enemies=enemies,
        weapon=weapon,
        target=target,
    )



async def range_attack_to_select_target(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
        weapon: WeaponItem | None,     # check cost
) -> str:
    return await player_range_attack.get_available_targets(
        game_model=game_model,
        room_model=game_model.room,
        enemies=enemies,
        weapon=weapon,
    )



async def range_attack(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
        weapon: WeaponItem | None,
        target: int | None,
) -> str:
    return await player_range_attack.range_attack(
        game_model=game_model,
        room_model=game_model.room,
        enemies=enemies,
        weapon=weapon,
        target=target,
    )



async def end_looting(
        game_model: GameModel,
        room_model: RoomModel,
) -> str:
    return await loot_enemies.end_looting(
        game_model=game_model,
        room_model=room_model,
    )


"""
    Handle func
"""


async def _home_room_handle(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
) -> str:
    # Обновление состояний для более плавного перехода, без повторного вызова эндпоинта
    if room_model.state == const.RoomStates.Battle.ALL_ENEMIES_DEAD:
        await loot_enemies.update_to_end_loot_if_second_call( room_model )
    # Именно в таком порядке, потому что ALL_ENEMIES_DIED при повторном вызове устанавливает конец END_OF_BATTLE
    if room_model.state == const.RoomStates.Battle.END_OF_BATTLE:
        await _handle_end_of_battle(game_model, room_model, enemies)


    # Выбор действия исходя из room_model.state
    if room_model.state == const.RoomStates.General.TEXT:
        next_state = await _get_state_after_text(room_model)
        return await room_text_action.get_room_text_and_update(
            game_model=game_model,
            room_model=room_model,
            next_state_if_no_text=next_state,
        )


    elif room_model.state == const.RoomStates.General.INIT:
        return await battle_starter.start_battle(
            game_model=game_model,
            room_model=room_model,
            enemies=enemies,
        )


    elif room_model.state == const.RoomStates.Battle.ENEMIES_BEFORE_PLAYER:
        return await enemies_turn.enemies_before_player(
            game_model=game_model,
            room_model=room_model,
            enemies=enemies,
        )


    elif room_model.state == const.RoomStates.Battle.PLAYER_TURN:
        return await player_turn.handle(
            game_model=game_model,
            room_model=room_model,
            enemies=enemies,
        )


    elif room_model.state == const.RoomStates.Battle.ENEMIES_AFTER_PLAYER:
        return await enemies_turn.enemies_after_player(
            game_model=game_model,
            room_model=room_model,
            enemies=enemies,
        )


    elif room_model.state == const.RoomStates.Battle.ALL_ENEMIES_DEAD:
        return await loot_enemies.home(
            game_model=game_model,
            room_model=room_model,
            enemies=enemies,
        )


    elif room_model.state == const.RoomStates.General.LEAVE:
        return await leave_room.leave_room(game_model)


    return (f"State '{room_model.state}' не обрабатывается.\n\n"
            f" file: {__file__}\n"
            f"  func:_handle_state")



"""
    Realization
"""


async def _handle_end_of_battle(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
):
    await _end_of_battle_trigger(game_model, enemies)

    is_string = room_text_action.unsafe_check_is_string(room_model)

    if is_string:
        room_model.state = const.RoomStates.General.LEAVE
        return

    text_pointer = state_manager.get_state_value(room_model, const.RoomStates.General.TEXT)

    if text_pointer > len(room_model.texts):
        room_model.state = const.RoomStates.General.LEAVE
        return

    room_model.state = const.RoomStates.General.TEXT



async def _end_of_battle_trigger(game_model: GameModel, enemies: list[MobModel]):
    for mob_model in enemies:
        await entity_script.execute_script_by_trigger(
            game_model=game_model,
            owner=mob_model,
            enemies=enemies,
            trigger=const.Trigger.CLOSE_BATTLE,
        )
    await entity_script.execute_script_by_trigger(
        game_model=game_model,
        owner=game_model.character,
        enemies=enemies,
        trigger=const.Trigger.CLOSE_BATTLE,
    )



async def _get_state_after_text(
        room_model: RoomModel,
) -> str:
    if len(room_model.enemies) == 0:
        return const.RoomStates.General.LEAVE

    encounter_pointer = state_manager.get_state_value(room_model, const.RoomStates.General.INIT)
    is_int = isinstance(room_model.enemies[0], int)

    if is_int:
        if encounter_pointer > 1:
            return const.RoomStates.General.LEAVE
        else:
            return const.RoomStates.General.INIT

    else:
        if encounter_pointer > len(room_model.enemies):
            return const.RoomStates.General.LEAVE
        else:
            return const.RoomStates.General.INIT
