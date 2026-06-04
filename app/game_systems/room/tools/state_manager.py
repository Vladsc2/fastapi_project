from fastapi import HTTPException, status
from app.models.room import RoomModel
from game_data import const

def get_state_value( room_model: RoomModel, state: str ) -> int:
    return room_model.updated_states.get(state, 1)


def increase_state_value( room_model: RoomModel, update_state: str, next_state: str, stoppers: list | None = None ):
    room_model.state = next_state
    if stoppers is None:
        room_model.stoppers = []
    else:
        room_model.stoppers = stoppers

    value = get_state_value(room_model, update_state)
    room_model.updated_states[update_state] = value + 1



def increase_current_state( room_model: RoomModel, next_state: str, stoppers: list | None = None ):
    increase_state_value(
        room_model=room_model,
        update_state=room_model.state,
        next_state=next_state,
        stoppers=stoppers
    )



def validate_state(room_model: RoomModel, expect_state: str, detail: str):
    if room_model.state != expect_state:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )



def validate_player_turn(room_model: RoomModel):
    validate_state(
        room_model=room_model,
        expect_state=const.RoomStates.Battle.PLAYER_TURN,
        detail="Сейчас не ход игрока"
    )