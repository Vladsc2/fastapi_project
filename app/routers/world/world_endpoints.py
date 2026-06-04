from fastapi import APIRouter, Query, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_interface import db_interface
from app.html_system import wrapper, form_error_text

from app.models.game import GameModel

from app.cruds.game import game_crud
from app.cruds.world import world_crud
from app.text_system.world import world_text
from game_data import const

router = APIRouter(prefix="/world", tags=["World"])


@router.get("", response_class=HTMLResponse)
async def create_profile_and_create_association(
        request: Request,
        session: AsyncSession = Depends(db_interface.get_session),
):
    ip_address = request.client.host

    try:
        game_model: GameModel = await game_crud.validate_major_state(
            ip_address=ip_address,
            state=const.WorldState.WORLD,
            session=session,
        )
    except HTTPException as error:
        return await form_error_text( error )


    text: str = world_text.get_world_text(
        base_url=request.base_url,
        world_model=game_model.world,
    )

    return await wrapper.wrap_pure( text )


