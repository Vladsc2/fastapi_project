from app.models.game import GameModel
from app.models.room import RoomModel
from game_data import const

"""
    Interfaces
"""

def get_exit_text(
        game_model: GameModel,
) -> str:

    string = ""
    if game_model.major_state == const.WorldState.ROOM:
        string = _get_denied_text(game_model)
    elif game_model.major_state == const.WorldState.RAID:
        string = _get_raid_text(game_model)
    elif game_model.major_state == const.WorldState.WORLD:
        string = _get_world_text(game_model)


    return string


"""
    Realization
"""

def _get_denied_text(
        game_model: GameModel,
) -> str:
    return """
            Не удалось покинуть данную локацию
    """



def _get_raid_text(
        game_model: GameModel,
) -> str:
    return """
            Вы успешно покинули локацию, и двинулись дальше
            
             <a href='/raid'>Рейд</a>
    """


def _get_world_text(
        game_model: GameModel,
) -> str:
    return """
            Вы вернулись в город.
             
            Теперь вам снова доступно свободное перемещение по миру
            
             <a href='/world'>Мир</a>
    """