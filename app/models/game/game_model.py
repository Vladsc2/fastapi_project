from app.models.base import BaseModel, BaseIdModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.general import ProfileModel
    from app.models.game import MainCharacterModel
    from app.models.world import WorldModel
    from app.models.raid import RaidModel, MetaModel
    from app.models.room import RoomModel
    from app.models.game import RollModel


class GameModel(BaseIdModel):
    __tablename__ = "games"

    character_id: Mapped[int] = mapped_column( ForeignKey("main_characters.id", onupdate="CASCADE") )

    major_state: Mapped[str | None] = mapped_column( default=None )
    world_id: Mapped[int ] = mapped_column( ForeignKey("world.id", onupdate="CASCADE") )
    raid_id: Mapped[int] = mapped_column( ForeignKey("raids.id", onupdate="CASCADE") )
    room_id: Mapped[int] = mapped_column( ForeignKey("rooms.id", onupdate="CASCADE") )

    meta_id: Mapped[int] = mapped_column( ForeignKey("meta.id", ondelete="CASCADE") )

    roll_id: Mapped[int] = mapped_column( ForeignKey("roll.id", ondelete="CASCADE") )


    character: Mapped["MainCharacterModel"] = relationship(
        back_populates="game",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True
    )
    world: Mapped["WorldModel"] = relationship(
        back_populates="game",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True
    )
    raid: Mapped["RaidModel"] = relationship(
        back_populates="game",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True
    )
    room: Mapped["RoomModel"] = relationship(
        back_populates="game",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True
    )

    meta: Mapped["MetaModel"] = relationship(
        back_populates="game",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True
    )

    roll: Mapped["RollModel"] = relationship(
        back_populates="game",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True
    )