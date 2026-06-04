from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.general import ProfileInputSchema
from app.models.general import IpAssociationsModel, ProfileModel

from app.cruds.general import abs_profile

"""
    CRUD Interfaces
"""

async def create_profile_and_login(
        ip_address: str,
        input_schema: ProfileInputSchema,
        session: AsyncSession,
) -> ProfileModel:
    profile_model: ProfileModel = await create_profile(
        ip_address=ip_address,
        input_schema=input_schema,
        session=session)

    await _set_ip_association(
        ip_address=ip_address,
        profile_id=profile_model.id,
        session=session,
    )

    return profile_model



async def create_profile(
        ip_address: str,
        input_schema: ProfileInputSchema,
        session: AsyncSession
) -> ProfileModel:
    await _check_free_name(name=input_schema.name, session=session)

    profile_model = await _create_new_profile(
        name=input_schema.name,
        passwords=input_schema.password,
        ip_address=ip_address,
        session=session,
    )

    return profile_model



async def login_profile(
        ip_address: str,
        input_schema: ProfileInputSchema,
        session: AsyncSession,
) -> ProfileModel:
    profile_model = await abs_profile.get_profile_by_name_and_password(
        name=input_schema.name,
        password=input_schema.password,
        session=session
    )

    await _set_ip_association(
        ip_address=ip_address,
        profile_id=profile_model.id,
        session=session
    )

    return profile_model





"""
    CRUD Realization
"""


async def _check_free_name(name: str, session: AsyncSession):
    statement = select(ProfileModel).where( ProfileModel.name == name )
    result: Result = await session.execute( statement )
    profile_model: ProfileModel | None = result.scalar_one_or_none()

    if profile_model is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Profile with name '{profile_model.name}' already exists"
        )



async def _create_new_profile(
        name: str,
        passwords: str,
        ip_address: str,
        session: AsyncSession
) -> ProfileModel:

    profile_model = ProfileModel(
        name=name,
        password=passwords,
        last_ip=ip_address,
    )
    session.add( profile_model )
    await session.commit()

    return profile_model



async def _set_ip_association(
        ip_address: str,
        profile_id: int,
        session: AsyncSession,
):

    statement = select(IpAssociationsModel).where(IpAssociationsModel.ip_address == ip_address)
    result: Result = await session.execute( statement )
    ip_association: IpAssociationsModel | None = result.scalar_one_or_none()

    if ip_association is None:
        ip_association = IpAssociationsModel(
            ip_address=ip_address,
            profile_id=profile_id
        )
        session.add( ip_association )

    else:
        ip_association.profile_id = profile_id

    await session.commit()