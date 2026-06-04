from fastapi import APIRouter, Query, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_interface import db_interface
from app.html_system import wrapper, form_error_text

from app.models import GameModel

from app.cruds.raid import raid_select_room_crud
from app.cruds.game import game_crud
from app.text_system.raid import raid_select_room_text
from game_data import const


router = APIRouter(prefix="/raid", tags=["Raid"])



@router.get("/select-{room_number}", response_class=HTMLResponse)
async def select_room(
        request: Request,
        room_number: int,
        session: AsyncSession = Depends(db_interface.get_session),
):
    ip_address = request.client.host

    try:
        game_model: GameModel = await game_crud.validate_major_state(
            ip_address=ip_address,
            state=const.WorldState.RAID,
            session=session,
        )

        await raid_select_room_crud.select_room(
            game_model=game_model,
            room_number=room_number,
            session=session,
        )

    except HTTPException as error:
        return await form_error_text( error )


    text: str = raid_select_room_text.get_text(
        room_number=room_number,
        room_model=game_model.room,
    )

    return await wrapper.wrap_pure( text )

