from app.models.game import GameModel
from app.models.raid import RaidModel, raid_model

from game_data import const


async def leave_room(game_model: GameModel):
    return await _leave_room(game_model)



async def _leave_room(game_model: GameModel) -> str:
    raid_model: RaidModel = game_model.raid

    if game_model.raid.current_line < len(game_model.raid.mesh):
        return await _step_into_raid(game_model, raid_model)
    else:
        return await _step_out_of_raid(game_model)



async def _step_into_raid(
        game_model: GameModel,
        raid_model: RaidModel,
):
    game_model.major_state = const.WorldState.RAID
    raid_model.current_line += 1

    return ("Вы покидаете локацию и двигаетесь дальше\n\n"
            " <a href='/raid'>Рейд</a>")



async def _step_out_of_raid(
        game_model: GameModel,
):
    game_model.major_state = const.WorldState.WORLD

    return ("Вы вышли из рейда\n\n"
            " <a href='/world'>Мир</a>")