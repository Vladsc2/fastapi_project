from app.models.base import BaseModel, BaseIdModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, JSON
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.game import MainCharacterModel


class InventoryModel(BaseIdModel):
    __tablename__ = "inventory"

    available_slots: Mapped[int] = mapped_column(default=5)
    content: Mapped[list] = mapped_column(JSON, default=list)

    character: Mapped["MainCharacterModel"] = relationship(back_populates="inventory")