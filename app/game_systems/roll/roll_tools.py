from fastapi import HTTPException, status
from app.models.game import RollModel
from game_data import const

def get_roll_list(
        roll_model: RollModel,
        roll_const: str,
) -> list[int]:
    if roll_const == const.Roll.ROLL_2:
        return roll_model.d2
    elif roll_const == const.Roll.ROLL_4:
        return roll_model.d4
    elif roll_const == const.Roll.ROLL_6:
        return roll_model.d6
    elif roll_const == const.Roll.ROLL_8:
        return roll_model.d8
    elif roll_const == const.Roll.ROLL_10:
        return roll_model.d10
    elif roll_const == const.Roll.ROLL_12:
        return roll_model.d12
    elif roll_const == const.Roll.ROLL_20:
        return roll_model.d20
    elif roll_const == const.Roll.ROLL_PERCENT:
        return roll_model.percent

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Не удалось получить список значений из RollModel по игровой константе '{roll_const}'"
    )



def update_roll_model_by_const(
        roll_model: RollModel,
        roll_const: str,
        value: int,
):
    if roll_const == const.Roll.ROLL_2:
        roll_model.d2 = roll_model.d2 + [value]
    elif roll_const == const.Roll.ROLL_4:
        roll_model.d4 = roll_model.d4 + [value]
    elif roll_const == const.Roll.ROLL_6:
        roll_model.d6 = roll_model.d6 + [value]
    elif roll_const == const.Roll.ROLL_8:
        roll_model.d8 = roll_model.d8 + [value]
    elif roll_const == const.Roll.ROLL_10:
        roll_model.d10 = roll_model.d10 + [value]
    elif roll_const == const.Roll.ROLL_12:
        roll_model.d12 = roll_model.d12 + [value]
    elif roll_const == const.Roll.ROLL_20:
        roll_model.d20 = roll_model.d20 + [value]
    elif roll_const == const.Roll.ROLL_PERCENT:
        roll_model.percent = roll_model.percent + [value]



def get_roll_dict(roll_model: RollModel) -> dict[str, list[int]]:
    return {
        const.Roll.ROLL_2: roll_model.d2.copy(),
        const.Roll.ROLL_4: roll_model.d4.copy(),
        const.Roll.ROLL_6: roll_model.d6.copy(),
        const.Roll.ROLL_8: roll_model.d8.copy(),
        const.Roll.ROLL_10: roll_model.d10.copy(),
        const.Roll.ROLL_12: roll_model.d12.copy(),
        const.Roll.ROLL_20: roll_model.d20.copy(),
        const.Roll.ROLL_PERCENT: roll_model.percent.copy(),
    }