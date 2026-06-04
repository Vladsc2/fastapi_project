from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.general import IpAssociationsModel, ProfileModel
from app.models.game import GameModel
from app.models.game import MainCharacterModel


async def get_active_game(
        ip_address: str,
        session: AsyncSession,
) -> GameModel:

    profile_model: ProfileModel = await _get_active_profile(ip_address, session)

    game_model: GameModel = await _get_active_game(profile_model, session)

    return game_model



async def _get_active_profile(
        ip_address: str,
        session: AsyncSession,
) -> ProfileModel:

    statement = select( IpAssociationsModel ).options(
        joinedload( IpAssociationsModel.profile )
    ).where( IpAssociationsModel.ip_address == ip_address )

    result: Result = await session.execute( statement )

    ip_association: IpAssociationsModel | None = result.scalar_one_or_none()

    if ip_association is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Данный ip адрес не зарегистрирован в системе\nСоздайте профиль, чтобы получить доступ к игре"
        )

    if ip_association.profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Профиль для данного адреса равен None. Для доступа к игре, создайте или войдите в профиль"
        )


    return ip_association.profile



async def _get_active_game(
        profile_model: ProfileModel,
        session: AsyncSession,
) -> GameModel:

    if profile_model.active_game_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Для профиля '{profile_model.name}' нет активной игры.\n"
                   f" Установите активную игру из доступных, или создайте новую!"
        )

    statement = select(GameModel).options(
        joinedload( GameModel.character )
        .joinedload( MainCharacterModel.char_equip ),
        joinedload( GameModel.character )
        .joinedload( MainCharacterModel.inventory ),
        joinedload( GameModel.world ),
        joinedload( GameModel.raid ),
        joinedload( GameModel.room ),
        joinedload( GameModel.meta ),
        joinedload( GameModel.roll )
    ).where( GameModel.id == profile_model.active_game_id )

    result: Result = await session.execute( statement )

    game_model = result.scalar_one_or_none()

    if game_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не удалось получить игру по полю в ProfileModel 'active_game_id'.\n"
                   "Это не стандартное поведение, и ссылка на активную игру всегда должна ссылаться на существующую\n"
                   "Обратитесь к администратору сервера"
        )

    return game_model