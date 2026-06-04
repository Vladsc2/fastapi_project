from app.models.base import BaseModel, BaseIdModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.game import GameModel


class WorldModel( BaseIdModel ):
    __tablename__ = "world"

    raid_goblin_forest_available: Mapped[bool] = mapped_column(default=True)
    raid_empire_caves: Mapped[bool] = mapped_column(default=False)
    raid_elven_ruins: Mapped[bool] = mapped_column(default=False)
    raid_tropical_islands: Mapped[bool] = mapped_column(default=False)
    raid_dead_city: Mapped[bool] = mapped_column(default=False)

    trader_available: Mapped[bool] = mapped_column(default=False)


    game: Mapped["GameModel"] = relationship(back_populates="world")