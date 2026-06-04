from fastapi import APIRouter, Query, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_interface import db_interface
from app.html_system import wrapper, form_error_text

from app.schemas.general import ProfilePasswordSchema
from app.models.general import ProfileModel

from app.cruds.general import profile_crud
from app.text_system.general import profile_text



router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/sign_out", response_class=HTMLResponse)
async def logout_from_profile(
        request: Request,
        session: AsyncSession = Depends(db_interface.get_session),
) -> str:
    ip_address: str = request.client.host

    try:

        await profile_crud.sign_out_profile(
            ip_address=ip_address,
            session=session,
        )

    except HTTPException as error:
        return await form_error_text(error)

    text = profile_text.get_sign_out_text()

    return await wrapper.wrap_pure( text )



@router.get("/delete", response_class=HTMLResponse)
async def delete_profile(
        request: Request,
        password_schema: ProfilePasswordSchema = Query(...),
        session: AsyncSession = Depends(db_interface.get_session),
) -> str:
    ip_address: str = request.client.host

    try:
        await profile_crud.delete_profile(
            ip_address=ip_address,
            password_schema=password_schema,
            session=session,
        )

    except HTTPException as error:
        return await form_error_text( error )

    text = profile_text.get_delete_profile_text()

    return await wrapper.wrap_pure( text )