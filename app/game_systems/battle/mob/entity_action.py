from app.models.game import GameModel
from app.models.game import MobModel


async def get_entities_before_player(
        game_model: GameModel,
        entities: list[MobModel]
) -> list[MobModel]:
    result = []
    player_initiative = game_model.character.current_initiative
    for mob_model in entities:
        if mob_model.current_initiative > player_initiative:
            result.append( mob_model )
    return result



async def get_entities_after_player(
        game_model: GameModel,
        entities: list[MobModel]
) -> list[MobModel]:
    result = []
    player_initiative = game_model.character.current_initiative
    for mob_model in entities:
        if mob_model.current_initiative <= player_initiative:
            result.append( mob_model )
    return result




async def do_entity_action(
        mob_model: MobModel,
) -> str:
    return f"{mob_model.name} выполнил действие\n\n"