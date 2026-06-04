from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game import GameModel
from app.models.raid import RaidModel
from app.schemas.room import RoomMeshSchema


"""
    CRUD Interfaces
"""

async def get_available_rooms(
        game_model: GameModel,
        session: AsyncSession
) -> list[RoomMeshSchema]:
    rooms: list[RoomMeshSchema] = await _get_available_rooms(
        game_model=game_model,
        session=session,
    )

    return rooms



async def get_raid_mesh(
            game_model: GameModel,
) -> list[list[list[RoomMeshSchema]]]:
    mesh: list[list[RoomMeshSchema]] = await _get_raid_mesh(game_model.raid)

    return mesh



"""
    CRUD Realization
"""

async def _get_available_rooms(
        game_model: GameModel,
        session: AsyncSession,
) -> list[RoomMeshSchema]:
    raid_model: RaidModel = game_model.raid

    line_index = raid_model.current_line - 1

    mesh: list[list[dict]] = raid_model.mesh
    if line_index < 0 or line_index >= len(mesh):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Указатель на линию в рейде указывает за пределы рейда\n"
                   f" - line_index: {line_index}\n"
                   f" - len(mesh):  {len(mesh)}"
        )

    line = mesh[line_index]

    new_line: list[RoomMeshSchema] = [ RoomMeshSchema( **room_dict ) for room_dict in line ]

    return new_line



async def _get_raid_mesh(
        raid_model: RaidModel,
) -> list[list[RoomMeshSchema]]:
    mesh: list[list[dict]] = raid_model.mesh

    mesh_view: list[list[RoomMeshSchema]] = [
        [RoomMeshSchema(**room) for room in line]
        for line in mesh
    ]

    return mesh_view