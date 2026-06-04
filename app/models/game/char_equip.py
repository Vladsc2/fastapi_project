from app.models.base import BaseModel, BaseIdModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, JSON
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.game import MainCharacterModel


class CharEquipModel(BaseIdModel):
    __tablename__ = "char_equips"

    close_weapon_url: Mapped[str] = mapped_column(default="")
    range_weapon_url: Mapped[str] = mapped_column(default="")

    armor_url: Mapped[str] = mapped_column(default="")

    ring_1_url: Mapped[str] = mapped_column(default="")
    ring_2_url: Mapped[str] = mapped_column(default="")
    amulet_url: Mapped[str] = mapped_column(default="")

    character: Mapped["MainCharacterModel"] = relationship(back_populates="char_equip")