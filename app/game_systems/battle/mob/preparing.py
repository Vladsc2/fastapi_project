from app.models.game import MobModel
from app.game_systems.character.stat import get_stat_modifier
from app.game_systems import roll
from game_data import const

async def roll_initiative(
        entities: list[MobModel]
):
    for entity in entities:
        initiative = roll.roll20() + get_stat_modifier(entity, const.Stat.Dexterity)
        entity.current_initiative = initiative