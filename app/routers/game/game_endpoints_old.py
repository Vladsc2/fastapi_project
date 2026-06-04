from fastapi import APIRouter, Request, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_interface import db_interface
from app.schemas.game import CreateGameSchema, GameAndCharSchema, GameSlotSchema, GameSchema
from app.schemas.base import StatusResponse
from app.cruds.game import init_game_crud, game_crud

router = APIRouter(prefix="/game", tags=["Game"])

@router.get("/create", response_model=GameAndCharSchema)
async def create_game(
        request: Request,
        input_schema: CreateGameSchema = Query(...),
        session: AsyncSession = Depends(db_interface.get_session),
):
    ip_address = request.client.host

    response = await init_game_crud.create_game(
        ip_address=ip_address,
        game_slot=input_schema.game_slot,
        player_name=input_schema.character_name,
        session=session
    )

    return response


@router.patch("/set_active", response_model=StatusResponse)
async def set_active_game(
        request: Request,
        slot_schema: GameSlotSchema = Query(...),
        session: AsyncSession = Depends(db_interface.get_session),
):
    ip_address = request.client.host

    await game_crud.set_active_game(
        ip_address=ip_address,
        slot=slot_schema.game_slot,
        session=session,
    )

    return StatusResponse(success=True)


@router.get("/acitve_game", response_model=GameSchema)
async def get_active_game(
        request: Request,
        session: AsyncSession = Depends(db_interface.get_session),
):
    ip_address = request.client.host

    game_model = await game_crud.get_active_game(
        ip_address=ip_address,
        session=session,
    )

    return game_model



@router.delete("/delete", response_model=StatusResponse)
async def delete_game(
        request: Request,
        slot_schema: GameSlotSchema = Query(...),
        session: AsyncSession = Depends(db_interface.get_session),
):
    ip_address = request.client.host

    await init_game_crud.delete_game(
        ip_address=ip_address,
        game_slot=slot_schema.game_slot,
        session=session,
    )

    return StatusResponse(success=True)