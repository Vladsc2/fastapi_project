from fastapi import APIRouter, Query, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_interface import db_interface
from app.html_system import wrapper, form_error_text

from app.schemas.general import ProfileInputSchema
from app.models.general import ProfileModel

from app.cruds.general import profile_auth_crud
from app.text_system.general import profile_auth_text



router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/sign_up", response_class=HTMLResponse)
async def create_profile_and_login(
        request: Request,
        input_schema: ProfileInputSchema = Query(...),
        session: AsyncSession = Depends(db_interface.get_session),
) -> str:
    ip_address: str = request.client.host

    try:

        profile_model: ProfileModel = await profile_auth_crud.create_profile_and_login(
            ip_address=ip_address,
            session=session,
            input_schema=input_schema,
        )

    except HTTPException as error:
        return await form_error_text(error)

    text = profile_auth_text.get_sign_up_text(
        profile_model=profile_model,
    )

    return await wrapper.wrap_pure( text )



@router.get("/sign_in", response_class=HTMLResponse)
async def login_profile(
        request: Request,
        input_schema: ProfileInputSchema = Query(...),
        session: AsyncSession = Depends(db_interface.get_session),
) -> str:
    ip_address: str = request.client.host

    try:
        profile_model: ProfileModel = await profile_auth_crud.login_profile(
            ip_address=ip_address,
            input_schema=input_schema,
            session=session,
        )

    except HTTPException as error:
        return await form_error_text(error)

    text = profile_auth_text.get_sign_in_text(
        profile_model=profile_model
    )

    return await wrapper.wrap_pure( text )





# @router.get("/sign_up_only", response_model=ProfileOutputSchema)
# async def create_pure_profile(
#         request: Request,
#         session: AsyncSession = Depends(db_interface.get_session),
#         input_schema: ProfileInputSchema = Query(...)
# ) -> dict:
#     ip_address: str = request.client.host
#
#     return await crud.only_create_new_profile(
#         ip_address=ip_address,
#         session=session,
#         input_schema=input_schema,
#     )
#
#
#
# @router.get("/current_profile", response_model=ProfileOutputSchema)
# async def get_current_profile(
#         request: Request,
#         session: AsyncSession = Depends(db_interface.get_session),
# ) -> dict:
#     return await read_crud.get_current_profile(
#         ip_address=request.client.host,
#         session=session,
#     )
#
#
#
# @router.get("/profiles", response_model=list[ProfileOutputSchema])
# async def get_all_profiles(
#         request: Request,
#         session: AsyncSession = Depends(db_interface.get_session),
# ) -> list[ProfileOutputSchema]:
#
#     return await crud.get_all_profiles(
#         ip_address=request.client.host,
#         session=session
#     )
#
#
#
# @router.get("/ip_associations", response_model=list[IpAssociationSchema])
# async def get_all_ip_associations(
#         request: Request,
#         session: AsyncSession = Depends(db_interface.get_session),
# ) -> list[IpAssociationSchema]:
#
#     return await crud.get_ip_associations(
#         ip_address=request.client.host,
#         session=session
#     )
#
#
#
# @router.get("/sign_in", response_model=IpAssociationAndProfileSchema)
# async def login_profile(
#         request: Request,
#         session: AsyncSession = Depends(db_interface.get_session),
#         input_schema: ProfileInputSchema = Query(...),
# ) -> IpAssociationAndProfileSchema:
#     ip_address: str = request.client.host
#
#     return await crud.login_profile(ip_address, session, input_schema)
#
#
#
# @router.get("/sign_out", response_model=StatusResponse)
# async def sign_out_profile(
#         request: Request,
#         session: AsyncSession = Depends(db_interface.get_session),
# ):
#     ip_address: str = request.client.host
#
#     await crud.sign_out_profile(ip_address, session)
#
#     return {"success": True}
#
#
#
# @router.delete("/delete", response_model=StatusResponse)
# async def delete_profile(
#         session: AsyncSession = Depends(db_interface.get_session),
#         input_schema: ProfileInputSchema = Query(...)
# ):
#     await crud.delete_profile(session, input_schema)
#
#     return {"success": True}