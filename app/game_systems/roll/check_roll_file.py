from app.models.game import GameModel, RollModel
from app.game_systems.roll import roll_tools


async def get_roll_list(
    game_model: GameModel,
    roll_const: str,
    times: int,
) -> list[int] | None:

    roll_model: RollModel = game_model.roll

    roll_list: list[int] = roll_tools.get_roll_list(
        roll_model=roll_model,
        roll_const=roll_const,
    )

    roll_list = roll_list[:times]

    if len(roll_list) != times:
        return None

    return roll_list


async def get_roll(
    game_model: GameModel,
    roll_const: str,
) -> int | None:

    roll_list = await get_roll_list(
        game_model=game_model,
        roll_const=roll_const,
        times=1
    )

    if roll_list is None:
        return None

    return roll_list[0]



async def get_roll_dict(
        game_model: GameModel,
) -> dict[str, list[int]]:
    roll_model: RollModel = game_model.roll
    return roll_tools.get_roll_dict( roll_model )