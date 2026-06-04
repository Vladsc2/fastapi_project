from app.models.game import BaseCharacterModel
from game_data import const

async def update_round_points(
        char: BaseCharacterModel,
):
    char.actions = char.actions_max
    char.bonus_actions = char.bonus_actions_max




async def write_off_cost(
        char: BaseCharacterModel,
        costs: dict[str, int]
):
    # costs: dict[const.Cost, int]

    for cost_type, cost_value in costs.items():

        if cost_type == const.Cost.ACTION:
            char.actions = char.actions - cost_value
            if char.actions < 0: char.actions = 0

        if cost_type == const.Cost.BONUS_ACTION:
            char.bonus_actions = char.bonus_actions_max - cost_value
            if char.bonus_actions < 0: char.bonus_actions = 0

        if cost_type == const.Cost.MANA:
            char.mana = char.mana - cost_value
            if char.mana < 0: char.mana = 0