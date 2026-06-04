from app.models.raid import RaidModel

from game_data.raids_data.goblin_forest import RaidGoblinForestGS
from game_data.templates.room import RoomGS


def get_start_raid_text(
    raid_model: RaidModel,
    mesh: list[list[dict]],
) -> str:

    if raid_model.name == RaidGoblinForestGS.name:
        return _get_goblin_forest_text(mesh)

    return ""



def _get_goblin_forest_text(mesh: list[list[dict]]) -> str:
    return f"""
        Вы входите в лес на окраине Имперского города.
        
        Здесь вас ожидают как опасные гоблины и другие противники
        Так и различные богатства...
        
        
        Вам предстоит пройти {len(mesh)} комнат
        
        <a href="/raid">Перейти к рейду</a>
    """


