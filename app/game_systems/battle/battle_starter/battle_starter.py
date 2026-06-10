from app.models.game import GameModel
from app.models.room import RoomModel
from app.models.game import MobModel

from app.game_systems.room.tools import stopper_checker
from game_data import const

from app.game_systems.battle.mob import preparing

from app.game_systems.battle.battle_starter import battle_starter_text
from app.game_systems.roll import clear_roll, get_roll

from app.game_systems.character.stat import get_stat_modifier

from app.game_systems.battle.round_manager import round_manager




async def start_battle(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
) -> str:

    if stopper_checker.check_stopper(room_model, None):
        return await _init_entity_initiative(game_model, room_model, enemies)

    elif stopper_checker.check_stopper(room_model, const.Stopper.Battle.AWAIT_USER_INITIATIVE):
        return await _check_player_initiative(game_model, room_model, enemies)


    return (f"Не удалось обработать событие во время инициализации битвы\n\n"
            f"  app/game_system/battle/battle_starter/battle_starter.py\n\n"
            f"  - state: {room_model.state}\n"
            f"  - stoppers: {room_model.stoppers}\n")




async def _init_entity_initiative(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
) -> str:
    await preparing.roll_initiative(enemies)
    await clear_roll(game_model, const.Roll.ROLL_20)
    room_model.stoppers = [const.Stopper.Battle.AWAIT_USER_INITIATIVE]

    return battle_starter_text.get_text_start(enemies)



async def _check_player_initiative(
        game_model: GameModel,
        room_model: RoomModel,
        enemies: list[MobModel],
) -> str:

    initiative: int | None = await get_roll(game_model, const.Roll.ROLL_20)

    if initiative is None:
        return battle_starter_text.get_text_start(enemies)

    modifier = get_stat_modifier(game_model.character, const.Stat.Dexterity)
    game_model.character.current_initiative = initiative + modifier

    await round_manager.start_round(
        game_model=game_model,
        room_model=room_model,
        enemies=enemies,
    )

    return battle_starter_text.get_text_player_initiative(
        game_model=game_model,
        initiative=initiative,
        enemies=enemies,
    )

