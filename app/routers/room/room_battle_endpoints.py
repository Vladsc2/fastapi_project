from fastapi import APIRouter, Query, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_interface import db_interface
from app.html_system import wrapper, form_error_text

from app.models.game import GameModel

from app.cruds.game import game_crud
from app.cruds.room.room_types import battle_room_crud
from game_data import const


router = APIRouter(prefix="/room", tags=["Room"])


@router.get("/end_turn", response_class=HTMLResponse)
async def end_turn(
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

        text: str = await battle_room_crud.end_player_turn(
            game_model=game_model,
            session=session
        )


    except HTTPException as error:
        return await form_error_text( error )


    return await wrapper.wrap_pure( text )



@router.get("/close_attack", response_class=HTMLResponse)
async def close_attack_to_select(
        request: Request,
        session: AsyncSession = Depends(db_interface.get_session),
) -> str:
    ip_address = request.client.host

    try:
        game_model: GameModel = await game_crud.validate_major_state(
            ip_address=ip_address,
            state=const.WorldState.ROOM,
            session=session,
        )

        text: str = await battle_room_crud.close_attack_to_select_target(
            game_model=game_model,
            session=session
        )


    except HTTPException as error:
        return await form_error_text( error )


    return await wrapper.wrap_pure( text )



@router.get("/close_attack-{target}", response_class=HTMLResponse)
async def close_attack(
        request: Request,
        target: int,
        session: AsyncSession = Depends(db_interface.get_session),
) -> str:
    ip_address = request.client.host

    try:
        game_model: GameModel = await game_crud.validate_major_state(
            ip_address=ip_address,
            state=const.WorldState.ROOM,
            session=session,
        )

        text: str = await battle_room_crud.close_attack(
            game_model=game_model,
            target=target,
            session=session
        )


    except HTTPException as error:
        return await form_error_text( error )


    return await wrapper.wrap_pure( text )



@router.get("/range_attack", response_class=HTMLResponse)
async def range_attack_to_select(
        request: Request,
        session: AsyncSession = Depends(db_interface.get_session),
) -> str:
    ip_address = request.client.host

    try:
        game_model: GameModel = await game_crud.validate_major_state(
            ip_address=ip_address,
            state=const.WorldState.ROOM,
            session=session,
        )

        text: str = await battle_room_crud.range_attack_to_select_target(
            game_model=game_model,
            session=session
        )


    except HTTPException as error:
        return await form_error_text( error )


    return await wrapper.wrap_pure( text )



@router.get("/range_attack-{target}", response_class=HTMLResponse)
async def close_attack(
        request: Request,
        target: int,
        session: AsyncSession = Depends(db_interface.get_session),
) -> str:
    ip_address = request.client.host

    try:
        game_model: GameModel = await game_crud.validate_major_state(
            ip_address=ip_address,
            state=const.WorldState.ROOM,
            session=session,
        )

        text: str = await battle_room_crud.range_attack(
            game_model=game_model,
            target=target,
            session=session
        )


    except HTTPException as error:
        return await form_error_text( error )


    return await wrapper.wrap_pure( text )