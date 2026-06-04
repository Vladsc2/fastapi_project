from app.models.base import BaseModel, BaseIdModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.game import GameModel


class MetaModel(BaseIdModel):
    __tablename__ = "meta"

    story_delay: Mapped[int] = mapped_column(default=0)
    story_room_path: Mapped[str] = mapped_column(default="game_data/story_rooms/raid_goblin_forest/1")


    game: Mapped["GameModel"] = relationship(back_populates="meta")