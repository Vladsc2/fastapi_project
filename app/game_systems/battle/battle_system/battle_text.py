from app.models import GameModel
from app.models.room import RoomModel
from app.models.game import MobModel, MainCharacterModel

from app.game_systems.character.stat import get_stat_modifier
from game_data import const

"""
    Interfaces
"""

def get_home_battle_text(
        player_char: MainCharacterModel,
        enemies: list[MobModel],
) -> str:
    text = _form_enemies_view(enemies)
    text += _get_player_state(player_char)
    text += _get_possible_actions()
    return text


def get_end_turn_battle_text(
        player_char: MainCharacterModel,
) -> str:
    text = _end_player_turn_text(player_char)
    return text



"""
    Parts
"""

def _form_enemies_view(
        enemies: list[MobModel]
) -> str:
    text = "Враги на локации:\n\n"
    for mob_model in enemies:
        text += f"  {mob_model.name}  lvl = {mob_model.lvl} | hp = {mob_model.hp} | mana = {mob_model.mana}\n"
    return text + "\n\n"


def _get_player_state(
        player_char: MainCharacterModel,
) -> str:
    return (f"Ваши характеристики:\n"
            f"  hp = {player_char.hp}, mana = {player_char.mana}\n"
            f"  actions = {player_char.actions}, bonus_actions = {player_char.bonus_actions}\n\n\n")


def _get_possible_actions(

) -> str:
    actions = [
        "<a href='/room/close_attack'>Атаковать оружием ближнего боя</a>",
        "<a href='/room/range_attack'>Атаковать оружием дальнего боя</a>",
        "Использовать заклинание",
        "Инвентарь",
        "<a href='/room/end_turn'>Закончить ход</a>"
    ]

    count = 1
    text = "Возможные действия:\n"
    for action in actions:
        text += "    " + action + "\n"

    return text + "\n"



def _end_player_turn_text(player_char: MainCharacterModel) -> str:
    text = f"{player_char.name} завершил ход\n\n"
    text += f" <a href='/room'>Далее</a>"
    return text