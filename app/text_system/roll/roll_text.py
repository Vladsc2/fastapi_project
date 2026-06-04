from app.models.game import GameModel
from app.models.game import RollModel
from app.game_systems.roll import roll_tools
from game_data import const
from game_data.const import const_modifier

def get_text(
        game_model: GameModel,
        roll_const: str,
        times: int,
) -> str:

    roll_model: RollModel = game_model.roll

    dice_name = const_modifier.get_readable_dice_name( roll_const )

    roll_list = roll_tools.get_roll_list(
        roll_model=game_model.roll,
        roll_const=roll_const,
    )
    roll_list = roll_list[-times:]

    text = f"Вы кинули кубик '{dice_name}' {_get_times_text(times)}\n\n"

    for index, roll_value in enumerate(roll_list):
        text += f"  Выпало: {roll_value}\n"


    back_url = roll_model.back_url
    if back_url is not None:
        text += f"\n\n <a href='{back_url}'>Назад</a>"

    return text




def _get_times_text(times: int) -> str:
    if times in (1, 5, 6, 7, 8, 9, 10):
        return f"{times} раз"
    else:
        return f"{times} раза"