from app.models.game import GameModel
from app.models.room import RoomModel
from app.models.game import MobModel

from app.game_systems.room.tools import state_manager
from app.game_systems.room.tools import stopper_checker

from game_data import const

"""
    Interface
"""

async def home(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
) -> str:
    if stopper_checker.check_stopper(room_model, None):
        return await _get_available_loot_targets(
            game_model=game_model,
            room_model=room_model,
            enemies=enemies,
        )

    return (f"Необработанное состояние в состоянии выбора цели для получения лута\n\n"
            f" - {__file__}\n"
            f" - state: {room_model.state}\n"
            f" - stoppers: {room_model.stoppers}\n")



async def update_to_end_loot_if_second_call(room_model: RoomModel) -> None:
    if stopper_checker.check_stopper(room_model, const.Stopper.Battle.AWAIT_SELECT_ENEMY_TO_LOOT):
        state_manager.increase_current_state(
            room_model=room_model,
            next_state=const.RoomStates.Battle.END_OF_BATTLE
        )


"""
    Realization
"""

async def _get_available_loot_targets(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
) -> str:
    state_manager.increase_current_state(
        room_model=room_model,
        next_state=room_model.state,
        stoppers=const.Stopper.Battle.AWAIT_SELECT_ENEMY_TO_LOOT,
    )

    text = "Выберите кого обыскать\n\n"
    for index, mob_model in enumerate(enemies):
        text += f" {index}) {mob_model.name}\n"
    text += f"\n\n <a href='/room'>Идти дальше</a>"
    return text
