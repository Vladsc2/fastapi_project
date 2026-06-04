from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game import GameModel
from app.schemas.room import RoomMeshSchema

from app.cruds.game import get_game_crud
from app.cruds.game import game_crud

from app.game_systems.raid import raid_creator
from game_data import const
from game_data.templates.raid import AbstractRaidGS


"""
    CRUD Interfaces
"""

async def create_raid(
        game_model: GameModel,
        raid_gs: AbstractRaidGS,
        session: AsyncSession,
):
    mesh: list[list[RoomMeshSchema]] = await raid_creator.form_raid_mesh(raid_gs)

    base_mesh: list[list[dict]] = await raid_creator.rooms_to_dict(mesh)

    await _update_raid_content(
        game_model=game_model,
        raid_gs=raid_gs,
        base_mesh=base_mesh,
        session=session,
    )

    await game_crud.set_major_state_game_model(
        game_model=game_model,
        state=const.WorldState.RAID,
        session=session,
    )




"""
    CRUD Realization
"""

async def _update_raid_content(
        game_model: GameModel,
        raid_gs: AbstractRaidGS,
        base_mesh: list[list[dict]],
        session: AsyncSession,
):
    raid_model: RaidModel = game_model.raid

    raid_model.name = raid_gs.name
    raid_model.desc = raid_gs.description

    raid_model.current_line = 1
    raid_model.mesh = base_mesh

    await session.commit()
