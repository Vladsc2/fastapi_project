from app.models.base import BaseModel, BaseIdModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, JSON
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.game import GameModel


class RaidModel(BaseIdModel):
    __tablename__ = "raids"

    name: Mapped[str] = mapped_column(default="")
    desc: Mapped[str] = mapped_column(default="")

    current_line: Mapped[int] = mapped_column(default=0)
    mesh: Mapped[list] = mapped_column(JSON, default=list)


    game: Mapped["GameModel"] = relationship(back_populates="raid")

