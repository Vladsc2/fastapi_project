from app.models.game import MobModel
from app.models.room import RoomModel
from app.game_systems.room.tools import state_manager
from game_data import const

def check_battle_win(
        room_model: RoomModel,
        enemies: list[MobModel],
) -> bool:
    _check_enemies_hp(room_model, enemies)



def _check_enemies_hp(room_model: RoomModel, enemies: list[MobModel]):
    for mob_model in enemies:
        if mob_model.hp > 0:
            return
    _set_next_state(  room_model, enemies )



def _set_next_state(room_model: RoomModel, enemies: list[MobModel]):
    has_loot = _check_enemies_loot(room_model, enemies)

    if has_loot:
        state_manager.increase_current_state(
            room_model=room_model,
            next_state=const.RoomStates.Battle.ALL_ENEMIES_DEAD,
        )
    else:
        state_manager.increase_current_state(
            room_model=room_model,
            next_state=const.RoomStates.Battle.END_OF_BATTLE
        )



def _check_enemies_loot(room_model: RoomModel, enemies: list[MobModel]) -> bool:
    for mob_model in enemies:
        for item_url in mob_model.loot:
            return True
    return False