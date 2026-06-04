from fastapi import APIRouter, Query, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_interface import db_interface
from app.html_system import wrapper, form_error_text

from app.models.game import GameModel

from app.cruds.game import game_crud
from app.cruds.room import room_exit_crud
from app.text_system.room import room_exit_text
from game_data import const



router = APIRouter(prefix="/room", tags=["Room"])


@router.get("/exit", response_class=HTMLResponse)
async def room_exit(
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

        await room_exit_crud.try_exit(game_model, session)

    except HTTPException as error:
        return await form_error_text( error )

    text = room_exit_text.get_exit_text(
        game_model=game_model
    )

    return await wrapper.wrap_pure( text )