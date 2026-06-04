from fastapi import HTTPException, status

from app.models.game import GameModel
from app.models.room import RoomModel
from app.models.game import MobModel

from app.game_systems.room.tools import state_manager
from app.game_systems.battle.mob import entity_action
from app.game_systems.character import points

from game_data import const


async def start_round(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
):
    if room_model.state == const.RoomStates.Battle.END_OF_BATTLE:
        return 

    before_enemies = await entity_action.get_entities_before_player(
        game_model=game_model,
        entities=enemies
    )

    if len(before_enemies) > 0:
        state_manager.increase_current_state(
            room_model=room_model,
            next_state=const.RoomStates.Battle.ENEMIES_BEFORE_PLAYER
        )
    else:
        await start_player_turn_actions(game_model, room_model)





async def start_player_turn_actions(
        game_model: GameModel,
        room_model: RoomModel,
):
    if room_model.state == const.RoomStates.Battle.END_OF_BATTLE:
        return

    state_manager.increase_current_state(
        room_model=room_model,
        next_state=const.RoomStates.Battle.PLAYER_TURN
    )

    await points.update_round_points( game_model.character )




async def end_player_turn(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
):
    after_enemies = await entity_action.get_entities_after_player(
        game_model=game_model,
        entities=enemies,
    )
    before_enemies = await entity_action.get_entities_before_player(
        game_model=game_model,
        entities=enemies
    )

    if len(after_enemies) > 0:
        next_state = const.RoomStates.Battle.ENEMIES_AFTER_PLAYER
    else:
        next_state = const.RoomStates.Battle.ENEMIES_BEFORE_PLAYER

    state_manager.increase_current_state(
        room_model=room_model,
        next_state=next_state
    )