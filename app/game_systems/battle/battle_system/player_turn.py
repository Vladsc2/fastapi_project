from app.models.game import GameModel
from app.models.room import RoomModel
from app.models.game import MobModel
from game_data import const

from app.game_systems.room.tools import stopper_checker
from app.game_systems.battle.round_manager import round_manager

from app.game_systems.battle.battle_system import battle_text

"""
    Interface
"""

async def handle(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
) -> str:
    await _clear_stoppers_if_back(room_model)

    if stopper_checker.check_stopper(room_model, None):
        return await _home_battle_text(
            game_model=game_model,
            room_model=room_model,
            enemies=enemies,
        )


    return (f"Не удалось обработать событие битвы\n\n"
                f"  app/game_system/battle/battle_system/battle_system.py\n\n"
                f"  - state: {room_model.state}\n"
                f"  - stoppers: {room_model.stoppers}\n")



async def end_player_turn(game_model: GameModel, enemies: list[MobModel]) -> str:
    return await _end_player_turn(game_model=game_model, enemies=enemies)



"""
    Realization
"""

async def _home_battle_text(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
) -> str:
    return battle_text.get_home_battle_text(
        player_char=game_model.character,
        enemies=enemies,
    )



async def _end_player_turn(game_model: GameModel, enemies: list[MobModel]) -> str:
    room_model: RoomModel = game_model.room

    await round_manager.end_player_turn(
        game_model=game_model,
        room_model=room_model,
        enemies=enemies,
    )

    return battle_text.get_end_turn_battle_text(game_model.character)



async def _clear_stoppers_if_back(
        room_model: RoomModel,
):
    if stopper_checker.check_stopper(room_model, const.Stopper.Battle.AWAIT_TARGET_CLOSE_ATTACK):
        room_model.stoppers = []
    elif stopper_checker.check_stopper(room_model, const.Stopper.Battle.AWAIT_TARGET_RANGE_ATTACK):
        room_model.stoppers = []