from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.general import IpAssociationsModel, ProfileModel


async def get_profile_by_name_and_password(
        name: str,
        password: str,
        session: AsyncSession,
) -> ProfileModel:

    statement = select(ProfileModel).where( ProfileModel.name == name )
    result: Result = await session.execute( statement )
    profile_model: ProfileModel | None = result.scalar_one_or_none()

    if profile_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with name '{name}' not found"
        )

    if profile_model.password != password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Incorrect password"
        )


    return profile_model

