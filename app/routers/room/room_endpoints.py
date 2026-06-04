from fastapi import APIRouter, Query, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_interface import db_interface
from app.html_system import wrapper, form_error_text

from app.models.game import GameModel

from app.cruds.game import game_crud
from app.cruds.room import room_crud
from game_data import const


router = APIRouter(prefix="/room", tags=["Room"])


@router.get("", response_class=HTMLResponse)
async def home_room(
        request: Request,
        session: AsyncSession = Depends(db_interface.get_session),
):
    ip_address = request.client.host

    try:
        game_model: GameModel = await game_crud.validate_major_state(
            ip_address=ip_address,
            state=const.WorldState.ROOM,
            session=session,
        )

        text: str = await room_crud.home_action(game_model, session)


    except HTTPException as error:
        return await form_error_text( error )


    return await wrapper.wrap_pure( text )




