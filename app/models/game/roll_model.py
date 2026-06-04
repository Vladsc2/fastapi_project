from app.models.base import BaseModel, BaseIdModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON, String, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.game import GameModel


class RollModel(BaseIdModel):
    __tablename__ = "roll"

    d2: Mapped[list] = mapped_column(JSON, default=list)
    d4: Mapped[list] = mapped_column(JSON, default=list)
    d6: Mapped[list] = mapped_column(JSON, default=list)
    d8: Mapped[list] = mapped_column(JSON, default=list)
    d10: Mapped[list] = mapped_column(JSON, default=list)
    d12: Mapped[list] = mapped_column(JSON, default=list)
    d20: Mapped[list] = mapped_column(JSON, default=list)
    percent: Mapped[list] = mapped_column(JSON, default=list)

    back_url: Mapped[str | None] = mapped_column(default=None)


    game: Mapped["GameModel"] = relationship(back_populates="roll")