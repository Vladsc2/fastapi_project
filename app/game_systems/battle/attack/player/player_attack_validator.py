from fastapi import HTTPException, status

from app.models.game import BaseCharacterModel
from game_data.templates.items import WeaponItem

from game_data import const

async def check_cost(
        char: BaseCharacterModel,
        weapon: WeaponItem,
) -> str | None:

    for cost_type, cost_value in weapon.costs.items():
        if cost_type == const.Cost.ACTION:
            if char.actions < cost_value:
                return (f"У Вас не хватает очков действий для использования '{weapon.name}'\n"
                        f" - Ваши действия: {char.actions}/{char.actions_max}\n"
                        f" - Необходимо для использования: {cost_value}\n\n"
                        f" <a href='/room'>Назад</a>")


        if cost_type == const.Cost.BONUS_ACTION:
            if char.bonus_actions < cost_value:
                return (f"У Вас не хватает бонусных действий для использования '{weapon.name}'\n"
                        f" - Ваши бонусные действия: {char.bonus_actions}/{char.bonus_actions_max}\n"
                        f" - Необходимо для использования: {cost_value}\n\n"
                        f" <a href='/room'>Назад</a>")


        if cost_type == const.Cost.MANA:
            if char.mana < cost_value:
                return (f"У Вас не хватает маны для использования '{weapon.name}'\n"
                        f"  - Ваша мана: {char.mana}/{char.mana_max}\n"
                        f" - Необходимо для использования: {cost_value}\n\n"
                        f" <a href='/room'>Назад</a>")