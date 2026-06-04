from app.models.game import MobModel
from app.models.room import RoomModel
from app.game_systems.room.tools import state_manager
from game_data import const

def check_battle_win(
        room_model: RoomModel,
) -> bool:
    if len(room_model.enemies) == 0:
        state_manager.increase_current_state(
            room_model=room_model,
            next_state=const.RoomStates.Battle.END_OF_BATTLE,
        )

    else:
        is_int = isinstance(room_model.enemies[0], int)

        if not is_int:
            pointer = state_manager.get_state_value(room_model, const.RoomStates.General.INIT) - 1
            enemy_list = room_model.enemies[pointer-1]
            if len(enemy_list) == 0:
                state_manager.increase_current_state(
                    room_model=room_model,
                    next_state=const.RoomStates.Battle.END_OF_BATTLE,
                )