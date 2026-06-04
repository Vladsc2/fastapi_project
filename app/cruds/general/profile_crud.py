from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.schemas.general import ProfilePasswordSchema
from app.models.general import ProfileModel, IpAssociationsModel


"""
    CRUD Interfaces
"""


async def get_ip_association(ip_address: str, raise_if_none: bool, session: AsyncSession) -> IpAssociationsModel | None:
    return await _get_ip_association( ip_address, raise_if_none, session )


async def get_profile_by_ip(ip_address: str, raise_if_none: bool, session: AsyncSession) -> ProfileModel | None:
    return await _get_active_profile( ip_address, raise_if_none, session )


async def sign_out_profile(
        ip_address: str,
        session: AsyncSession,
):
    """
        Sign Out
    """
    await _sign_out_profile(ip_address, session)



async def delete_profile(
        ip_address: str,
        password_schema: ProfilePasswordSchema,
        session: AsyncSession,
):

    await _delete_profile(
        ip_address=ip_address,
        password=password_schema.password,
        session=session
    )




"""
    CRUD Realization
"""


"""
    More specific
"""

async def _get_ip_association(
        ip_address: str,
        raise_if_none: bool,
        session: AsyncSession,
) -> IpAssociationsModel | None:
    statement = select(IpAssociationsModel).options(
        joinedload(IpAssociationsModel.profile)
    ).where( IpAssociationsModel.ip_address == ip_address )
    result: Result = await session.execute(statement)
    ip_association: IpAssociationsModel | None = result.scalar_one_or_none()

    if raise_if_none and ip_association is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"IP address '{ip_address}' not registered in data base"
        )

    return ip_association



async def _get_active_profile(
        ip_address: str,
        raise_if_none: bool,
        session: AsyncSession,
) -> ProfileModel | None:
    ip_association: IpAssociationsModel | None = await _get_ip_association(ip_address, raise_if_none, session)

    if ip_association is None:
        return None

    profile: ProfileModel | None = ip_association.profile

    if raise_if_none and profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No profile is associate with this ip '{ip_address}'"
        )

    return profile



async def _sign_out_profile(
        ip_address: str,
        session: AsyncSession,
):

    ip_association: IpAssociationsModel | None = await _get_ip_association(
        ip_address=ip_address,
        raise_if_none=True,
        session=session,
    )

    ip_association.profile_id = None
    await session.commit()



async def _delete_profile(
        ip_address: str,
        password: str,
        session: AsyncSession,
):

    ip_association: IpAssociationsModel = await _get_ip_association(
        ip_address=ip_address,
        raise_if_none=True,
        session=session,
    )

    profile_model: ProfileModel | None = ip_association.profile

    if profile_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Для удаления аккаунта, нужно в него войти"
        )

    if profile_model.password != password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect password"
        )

    await session.delete( profile_model )
    await session.commit()