from app.models.game import GameModel
from app.models.room import RoomModel
from app.models.game import MobModel
from game_data.templates.items import WeaponItem
from game_data import const

from app.game_systems.room.tools import state_manager

from app.game_systems.room.abstract_actions import room_text
from app.game_systems.battle.battle_starter import battle_starter
from app.game_systems.battle.battle_system import enemies_turn
from app.game_systems.battle.battle_system import player_turn
from app.game_systems.battle.attack.player import player_close_attack
from app.game_systems.battle.attack.player import player_range_attack
from app.game_systems.room.enter_leave import leave_room


"""
    Interfaces
"""

async def apply_next_state(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
) -> str:
    string = await _handle_state(game_model, room_model, enemies)

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




"""
    Realization
"""


async def _handle_state(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
) -> str:
    if room_model.state == const.RoomStates.Battle.END_OF_BATTLE:
        await _handle_end_of_battle(game_model, room_model)



    if room_model.state == const.RoomStates.General.TEXT:
        next_state = await _get_state_after_text(room_model)
        return await room_text.get_room_text_and_update(
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


    elif room_model.state == const.RoomStates.General.LEAVE:
        return await leave_room.leave_room(game_model)


    return (f"State '{room_model.state}' не обрабатывается.\n"
            f" app/game_system/room/room_actions/battle_room_actions.py'  func:_handle_state")




async def _handle_end_of_battle(
        game_model: GameModel,
        room_model: RoomModel,
):
    is_string = room_text.unsafe_check_is_string(room_model)

    if is_string:
        room_model.state = const.RoomStates.General.LEAVE
        return

    text_pointer = state_manager.get_state_value(room_model, const.RoomStates.General.TEXT)

    if text_pointer > len(room_model.texts):
        room_model.state = const.RoomStates.General.LEAVE
        return

    room_model.state = const.RoomStates.General.TEXT



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
