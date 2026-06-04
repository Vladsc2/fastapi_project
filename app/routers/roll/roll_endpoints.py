from fastapi import APIRouter, Query, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_interface import db_interface
from app.html_system import wrapper, form_error_text

from app.models import GameModel
from app.schemas.roll import RollSchema, RollSchemaTimes

from app.cruds.game import get_game_crud
from app.cruds.roll import roll_crud
from app.text_system.roll import roll_text

from game_data import const


router = APIRouter(prefix="/roll", tags=["Raid"])


@router.get("", response_class=HTMLResponse)
async def roll_dice(
        request: Request,
        roll_schema: RollSchemaTimes = Query(...),
        session: AsyncSession = Depends(db_interface.get_session),
):
    ip_address = request.client.host
    previous_url = request.headers.get("Referer", None)

    try:
        game_model: GameModel = await get_game_crud.get_active_game(
            ip_address=ip_address,
            session=session,
        )

        await roll_crud.save_back_url_if_not_roll(
            game_model=game_model,
            back_url=previous_url,
            session=session
        )

        roll_const: str = await _schema_dice_to_dice_const( roll_schema )
        times = roll_schema.times

        await roll_crud.roll_by_constant(
            game_model=game_model,
            roll_const=roll_const,
            times=times,
            session=session,
        )

    except HTTPException as error:
        return await form_error_text( error )

    text: str = roll_text.get_text(
        game_model=game_model,
        roll_const=roll_const,
        times=times,
    )

    return await wrapper.wrap_pure( text )



async def _schema_dice_to_dice_const(
        schema: RollSchema,
) -> str:
    if schema.dice == "2":
        return const.Roll.ROLL_2
    elif schema.dice == "4":
        return const.Roll.ROLL_4
    elif schema.dice == "6":
        return const.Roll.ROLL_6
    elif schema.dice == "8":
        return const.Roll.ROLL_8
    elif schema.dice == "10":
        return const.Roll.ROLL_10
    elif schema.dice == "12":
        return const.Roll.ROLL_12
    elif schema.dice == "20":
        return const.Roll.ROLL_20
    elif schema.dice == "percent":
        return const.Roll.ROLL_PERCENT

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Не удалось привести поле сходной схемы dice '{schema.dice}' к константе броска кубика\n\n"
               f" app/routers/roll/rool_endpoints.py"
    )