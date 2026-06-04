from app.models.game import GameModel, RollModel
from app.models.room import RoomModel
from game_data import const


async def clear_all_rolls(
        game_model: GameModel,
):
    roll_model: RollModel = game_model.roll

    roll_model.d2 = []
    roll_model.d4 = []
    roll_model.d6 = []
    roll_model.d8 = []
    roll_model.d10 = []
    roll_model.d12 = []
    roll_model.d20 = []
    roll_model.percent = []



async def clear_roll(
        game_model: GameModel,
        roll_const: str,
):
    roll_model: RollModel = game_model.roll

    if roll_const == const.Roll.ROLL_2:
        roll_model.d2 = []

    elif roll_const == const.Roll.ROLL_4:
        roll_model.d4 = []

    elif roll_const == const.Roll.ROLL_6:
        roll_model.d6 = []

    elif roll_const == const.Roll.ROLL_8:
        roll_model.d8 = []

    elif roll_const == const.Roll.ROLL_10:
        roll_model.d10 = []

    elif roll_const == const.Roll.ROLL_12:
        roll_model.d12 = []

    elif roll_const == const.Roll.ROLL_20:
        roll_model.d20 = []

    elif roll_const == const.Roll.ROLL_PERCENT:
        roll_model.percent = []