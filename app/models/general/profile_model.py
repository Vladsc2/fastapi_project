from typing import TYPE_CHECKING
from app.models.base import BaseModel, BaseIdModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from game_data import const

if TYPE_CHECKING:
    from app.models.general.ip_associations import IpAssociationsModel
    from app.models.game import GameModel

class ProfileModel(BaseIdModel):
    __tablename__ = "profiles"

    name: Mapped[str] = mapped_column( String(40) )
    password: Mapped[str] = mapped_column( String(140) )
    last_ip: Mapped[str]

    first_game_id: Mapped[int | None]
    second_game_id: Mapped[int | None]
    third_game_id: Mapped[int | None]

    active_game_id: Mapped[int | None]

    permissions: Mapped[str] = mapped_column(default=const.Permissions.PLAYER)


    ip_associations: Mapped[list["IpAssociationsModel"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan"
    )