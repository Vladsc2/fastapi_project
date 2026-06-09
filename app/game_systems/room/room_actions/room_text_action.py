import html
from fastapi import HTTPException, status
from app.models.game import GameModel
from app.models.room import RoomModel
from app.models.game import MobModel
from app.game_systems.room.tools import state_manager

from game_data import const

"""
    Interfaces
"""

async def get_room_text_and_update(
        game_model: GameModel,
        room_model: RoomModel,
        next_state_if_no_text: str,
) -> str:
    is_string, text_global_count = await _validate_texts(room_model)

    string = await _get_text(
        room_model=room_model,
        is_string=is_string,
        text_global_count=text_global_count,
    )

    await _update_room_model(
        room_model=room_model,
        is_string=is_string,
        text_global_count=text_global_count,
        next_state=next_state_if_no_text
    )

    string += '\n\n <a href="/room">Далее</a>'

    return string


def unsafe_check_is_string( room_model: RoomModel ) -> bool:
    return isinstance(room_model.texts[0], str)


"""
    Realization
"""


async def _get_text(
        room_model: RoomModel,
        is_string: bool,
        text_global_count: int,
) -> str:

    if is_string:
        return room_model.texts[ room_model.text_pointer - 1 ]

    else:
        return room_model.texts[ text_global_count-1 ][ room_model.text_pointer - 1 ]




async def _update_room_model(
        room_model: RoomModel,
        is_string: bool,
        text_global_count: int,
        next_state: str,
):
    room_model.text_pointer += 1

    if is_string:
        if room_model.text_pointer > len(room_model.texts):
            room_model.text_pointer = 1
            state_manager.increase_state_value(
                room_model=room_model,
                update_state=const.RoomStates.General.TEXT,
                next_state=next_state,
            )

    else:
        if room_model.text_pointer > len(room_model.texts[ text_global_count-1 ]):
            room_model.text_pointer = 1
            state_manager.increase_state_value(
                room_model=room_model,
                update_state=const.RoomStates.General.TEXT,
                next_state=next_state,
            )






"""
    Checks
"""

async def _validate_texts(
        room_model: RoomModel,
) -> tuple[bool, int]:
    await _validate_not_empty_texts(room_model)

    is_string = await _check_its_string(room_model.texts)

    text_count = state_manager.get_state_value(room_model, const.RoomStates.General.TEXT)

    await _validate_length_texts(
        room_mode=room_model,
        is_string=is_string,
        text_count=text_count,
    )

    return is_string, text_count



async def _validate_not_empty_texts(
        room_model: RoomModel,
):
    if len(room_model.texts) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"""
                Ошибка при получении текста комнаты
                    - state = '{room_model.state}'
                    - len(texts) == 0
            """
        )



async def _check_its_string(
        texts: list,
) -> bool:
    first_element_type = type( texts[0] )

    for el in texts:
        if not isinstance(el, first_element_type):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=html.escape(
                    f"Элементы массива texts имеют разный тип\n"
                    f"  - first_element: {first_element_type}\n"
                    f"  - other_element: {type(el)}\n"
                )
            )

    if first_element_type == str:
        return True
    return False



async def _validate_length_texts(
        room_mode: RoomModel,
        is_string: bool,
        text_count: int,
):

    if is_string:
        if text_count > 1:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Указатель для получения текста указывает на второй массив.\n"
                       "Но массив текста не состоит из вложенных массивов (чистый текст)\n"
            )
        if room_mode.text_pointer > len(room_mode.texts):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Указатель на текст указывает за пределы массива\n"
                       f"   - text_pointer = {room_mode.text_pointer}\n"
                       f"   - len(texts) = {len(room_mode.texts)}\n"
            )

    else:
        if text_count > len(room_mode.texts):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Указатель для получения массива текста указывает за пределы массива texts\n"
                       f"   - text_count = {text_count} (указатель на массив)\n"
                       f"   - len(texts) = {len(room_mode.texts)} (кол-во массивов)\n"
            )

        if room_mode.text_pointer > len( room_mode.texts[ text_count-1 ] ):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Указатель внутри вложенного массива, выходит за его пределы\n"
                       f"   - text_pointer = {room_mode.text_pointer}\n"
                       f"   - len( room_mode.texts[ text_count-1 ] ) = {len( room_mode.texts[ text_count-1 ] )}"
            )