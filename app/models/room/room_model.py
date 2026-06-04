from app.models.base import BaseModel, BaseIdModel
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableList, MutableDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.game import GameModel


class RoomModel(BaseIdModel):
    __tablename__ = "rooms"

    room_type: Mapped[str] = mapped_column(default="")
    room_path: Mapped[str] = mapped_column(default="")

    name: Mapped[str] = mapped_column(default="")

    text_pointer: Mapped[int] = mapped_column(default=0)
    texts: Mapped[list] = mapped_column(MutableList.as_mutable(JSON), default=list)

    stoppers: Mapped[list] = mapped_column(MutableList.as_mutable(JSON), default=list)
    state: Mapped[str] = mapped_column(default="")
    updated_states: Mapped[dict] = mapped_column(MutableDict.as_mutable(JSON), default=dict)

    enemies: Mapped[list] = mapped_column(MutableList.as_mutable(JSON), default=list)
    loot: Mapped[list] = mapped_column(MutableList.as_mutable(JSON), default=list)

    can_exit: Mapped[bool] = mapped_column(default=True)


    game: Mapped["GameModel"] = relationship(back_populates="room")