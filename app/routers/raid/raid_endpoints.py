from fastapi import APIRouter, Query, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_interface import db_interface
from app.html_system import wrapper, form_error_text

from app.models import GameModel

from app.cruds.raid import raid_crud
from app.cruds.game import game_crud
from app.text_system.raid import raid_text
from game_data import const


router = APIRouter(prefix="/raid", tags=["Raid"])


@router.get("", response_class=HTMLResponse)
async def raid_home(
        request: Request,
        session: AsyncSession = Depends(db_interface.get_session),
):
    ip_address = request.client.host

    try:
        game_model: GameModel = await game_crud.validate_major_state(
            ip_address=ip_address,
            state=const.WorldState.RAID,
            session=session,
        )

        rooms = await raid_crud.get_available_rooms(game_model, session)
    except HTTPException as error:
        return await form_error_text( error )

    text: str = raid_text.get_raid_state_text(
        game_model.raid,
        rooms,
    )

    return await wrapper.wrap_pure( text )



@router.get("/print_mesh", response_class=HTMLResponse)
async def print_raid_mesh(
        request: Request,
        session: AsyncSession = Depends(db_interface.get_session),
) -> str:
    ip_address = request.client.host

    try:
        game_model: GameModel = await game_crud.validate_major_state(
            ip_address=ip_address,
            state=const.WorldState.RAID,
            session=session,
        )

        mesh = await raid_crud.get_raid_mesh(
            game_model=game_model,
        )

    except HTTPException as error:
        return await form_error_text( error )


    text: str = raid_text.get_raid_mesh_text(
        raid_model=game_model.raid,
        mesh=mesh,
    )

    return await wrapper.wrap_pure( text )