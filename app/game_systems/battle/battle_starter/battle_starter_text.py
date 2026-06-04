from app.models import GameModel, room
from app.models.room import RoomModel
from app.models.game import MobModel
from app.game_systems.character.stat import get_stat_modifier
from game_data import const

def get_text_start(enemies: list[MobModel], add_next: bool = True) -> str:
    text = _get_start_text()
    text += _get_enemies_text(enemies)
    text += _get_player_initiative_text()
    if add_next:
        text += get_next_text()

    return text


def get_text_player_initiative(game_model: GameModel, initiative: int, enemies: list[MobModel]) -> str:
    text = get_text_start(enemies, False)
    text += _initiative_player_text(game_model, initiative)
    text += get_next_text()

    return text


def get_next_text() -> str:
    return f'\n\n <a href="/room">Далее</a>'


"""
    Text parts
"""

def _get_start_text() -> str:
    return "Начинается битва\n\n"

def _get_enemies_text(enemies: list[MobModel]) -> str:
    text = "Определение инициативы. Инициатива = d20 + модификатор ловкости\n\n"
    for mob_model in enemies:
        modifier = get_stat_modifier(mob_model, const.Stat.Dexterity)
        text += (f"  {mob_model.name} бросает на инициативу\n"
                 f"    Выпадает {mob_model.current_initiative - modifier}\n"
                 f"    Модификатор ловкости {modifier}\n"
                 f"    Инициатива: {mob_model.current_initiative}\n")
    text += "\n"
    return text


def _get_player_initiative_text() -> str:
    return f"Кидайте на инициативу\n"


def _initiative_player_text(game_model: GameModel, initiative: int) -> str:
    char = game_model.character
    text = f"\n  {char.name} бросает на инициативу\n"
    modifier = get_stat_modifier(char, const.Stat.Dexterity)
    text += f"    Выпадает {game_model.character.current_initiative - modifier}\n"
    text += f"    Модификатор ловкости {modifier}\n"
    text += f"    Инициатива: {char.current_initiative}\n"
    text += "\n"
    return text