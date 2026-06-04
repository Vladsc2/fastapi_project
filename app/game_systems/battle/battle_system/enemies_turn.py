from app.models.game import GameModel
from app.models.room import RoomModel
from app.models.game import MobModel

from app.game_systems.room.tools import stopper_checker
from game_data import const

from app.game_systems.battle.mob import entity_action
from app.game_systems.battle.round_manager import round_manager
from app.game_systems.character import entity_effects

"""
    Interfaces
"""

async def enemies_before_player(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
) -> str:
    if stopper_checker.check_stopper(room_model, None):
        return await _enemies_before_player(game_model, room_model, enemies)

    return (f"Не удалось обработать событие во время хода противников, с инициативой больше чем у игрока\n\n"
            f"  - {__file__}\n\n"
            f"  - state: {room_model.state}\n"
            f"  - stoppers: {room_model.stoppers}\n")



async def enemies_after_player(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
) -> str:
    if stopper_checker.check_stopper(room_model, None):
        return await _enemies_after_player(game_model, room_model, enemies)


    return (f"Не удалось обработать событие во время хода противников, с инициативой меньше чем у игрока\n\n"
            f"  - {__file__}\n\n"
            f"  - state: {room_model.state}\n"
            f"  - stoppers: {room_model.stoppers}\n")




"""
    Realization
"""

async def _enemies_before_player(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
) -> str:
    before_enemies = await entity_action.get_entities_before_player( game_model, enemies )
    text = ""
    for mob_model in before_enemies:
        text += await _entity_action(
            game_model=game_model,
            room_model=room_model,
            mob_model=mob_model,
        )

    await round_manager.start_player_turn_actions(
        game_model=game_model,
        room_model=room_model,
    )

    text += "\n <a href='/room'>Далее</a>\n\n"

    return text



async def _enemies_after_player(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
) -> str:
    after_enemies = await entity_action.get_entities_after_player( game_model, enemies )
    text = ""
    for mob_model in after_enemies:
        text += await _entity_action(
            game_model=game_model,
            room_model=room_model,
            mob_model=mob_model,
        )

    await round_manager.start_round(
        game_model=game_model,
        room_model=room_model,
        enemies=enemies
    )

    text += "\n <a href='/room'>Далее</a>\n\n"

    return text



async def _entity_action(
        game_model: GameModel,
        room_model: RoomModel,
        mob_model: MobModel,
):
    text = ""
    text += await entity_effects.apply_effects_on_entity(
        game_model=game_model,
        entity=mob_model,
        event=const.Event.START_TURN,
    )
    text += await entity_action.do_entity_action(
        mob_model=mob_model
    )
    text += await entity_effects.apply_effects_on_entity(
        game_model=game_model,
        entity=mob_model,
        event=const.Event.END_TURN,
    )

    return text