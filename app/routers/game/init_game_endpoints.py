from fastapi import APIRouter, Query, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_interface import db_interface
from app.html_system import wrapper, form_error_text

from app.schemas.game import CreateGameSchema, GameSlotSchema
from app.models.game import GameModel

from app.cruds.game import init_game_crud
from app.text_system.game import init_game_text


router = APIRouter(prefix="/game", tags=["Init Game"])


@router.get("/create", response_class=HTMLResponse)
async def create_game(
        request: Request,
        create_schema: CreateGameSchema = Query(...),
        session: AsyncSession = Depends(db_interface.get_session),
) -> str:
    ip_address: str = request.client.host

    try:
        game_model: GameModel = await init_game_crud.create_game(
            ip_address=ip_address,
            game_slot=create_schema.game_slot,
            player_name=create_schema.character_name,
            session=session
        )

    except HTTPException as error:
        return await form_error_text(error)

    text = init_game_text.get_create_game_text(
        game_slot=create_schema.game_slot,
        game_model=game_model,
    )

    return await wrapper.wrap_pure( text )



@router.get("/set_active", response_class=HTMLResponse)
async def set_active_game(
        request: Request,
        slot_schema: GameSlotSchema = Query(...),
        session: AsyncSession = Depends(db_interface.get_session),
) -> str:
    ip_address: str = request.client.host

    try:
        game_id: int = await init_game_crud.set_active_game(
            ip_address=ip_address,
            game_slot=slot_schema.game_slot,
            session=session
        )
    except HTTPException as error:
        return await form_error_text(error)

    text = init_game_text.get_set_active_game_text(
        game_slot=slot_schema.game_slot,
        game_id=game_id
    )

    return await wrapper.wrap_pure( text )


@router.get("/delete", response_class=HTMLResponse)
async def delete_game(
        request: Request,
        slot_schema: GameSlotSchema = Query(...),
        session: AsyncSession = Depends(db_interface.get_session),
) -> str:
    ip_address: str = request.client.host

    try:
        game_id: int =  await init_game_crud.delete_game(
            ip_address=ip_address,
            game_slot=slot_schema.game_slot,
            session=session
        )
    except HTTPException as error:
        return await form_error_text(error)

    text = init_game_text.get_delete_game_text(
        game_slot=slot_schema.game_slot,
        game_id=game_id
    )

    return await wrapper.wrap_pure( text )