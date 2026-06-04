from fastapi import APIRouter, Query, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_interface import db_interface
from app.html_system import wrapper, form_error_text

from app.models.game import GameModel

from app.cruds.world import world_create_raid_crud
from app.cruds.game import game_crud
from app.text_system.world import world_start_raid_text

from game_data.raids_data.goblin_forest import RaidGoblinForestGS
from game_data import const


router = APIRouter(prefix="/world/start_raid", tags=["World"])


@router.get("/goblin_forest", response_class=HTMLResponse)
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

        await world_create_raid_crud.create_raid(
            game_model=game_model,
            raid_gs=RaidGoblinForestGS,
            session=session
        )

    except HTTPException as error:
        return await form_error_text( error )


    text = world_start_raid_text.get_start_raid_text(
        raid_model=game_model.raid,
        mesh=game_model.raid.mesh
    )

    return await wrapper.wrap_pure( text )


