from app.models.base import BaseModel, BaseIdModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, JSON
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.game import GameModel
    from app.models.game import CharEquipModel, InventoryModel


class BaseCharacterModel( BaseIdModel ):
    __abstract__ = True

    name: Mapped[str] = mapped_column(String(30))
    lvl: Mapped[int] = mapped_column(default=1)

    hp: Mapped[int] = mapped_column(default=9)
    mana: Mapped[int] = mapped_column(default=0)
    mana_max: Mapped[int] = mapped_column(default=0)

    actions: Mapped[int] = mapped_column(default=1)
    actions_max: Mapped[int] = mapped_column(default=1)
    bonus_actions: Mapped[int] = mapped_column(default=1)
    bonus_actions_max: Mapped[int] = mapped_column(default=1)

    prepared_spell_1_id: Mapped[int | None] = mapped_column(default=None)
    prepared_spell_2_id: Mapped[int | None] = mapped_column(default=None)
    prepared_spell_3_id: Mapped[int | None] = mapped_column(default=None)
    prepared_spell_4_id: Mapped[int | None] = mapped_column(default=None)
    prepared_spell_5_id: Mapped[int | None] = mapped_column(default=None)
    prepared_spell_6_id: Mapped[int | None] = mapped_column(default=None)
    available_spells: Mapped[int] = mapped_column(default=0)

    stat_strength: Mapped[int] = mapped_column(default=7)
    stat_dexterity: Mapped[int] = mapped_column(default=7)
    stat_constitution: Mapped[int] = mapped_column(default=7)
    stat_intelligence: Mapped[int] = mapped_column(default=7)
    stat_will: Mapped[int] = mapped_column(default=7)

    current_initiative: Mapped[int] = mapped_column(default=0)

    effects: Mapped[list] = mapped_column(JSON, default=list)
    scripts: Mapped[list] = mapped_column(JSON, default=list)



class MobModel( BaseCharacterModel ):
    __tablename__ = "mobs"

    desc: Mapped[str] = mapped_column(default="")

    weapon_url: Mapped[str] = mapped_column(default="")
    armor_url: Mapped[str] = mapped_column(default="")

    exp: Mapped[float] = mapped_column(default=0)
    loot: Mapped[list] = mapped_column(JSON, default=list)



class MainCharacterModel( BaseCharacterModel ):
    __tablename__ = "main_characters"

    energy: Mapped[float] = mapped_column(default=5)
    max_energy: Mapped[float] = mapped_column(default=5)
    energy_per_minute: Mapped[float] = mapped_column(default=0.06)

    char_equip_id: Mapped[int] = mapped_column( ForeignKey("char_equips.id", ondelete="CASCADE") )
    inventory_id: Mapped[int] = mapped_column( ForeignKey("inventory.id", ondelete="CASCADE") )


    game: Mapped["GameModel"] = relationship(back_populates="character")

    char_equip: Mapped["CharEquipModel"] = relationship(
        back_populates="character",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True
    )

    inventory: Mapped["InventoryModel"] = relationship(
        back_populates="character",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True
    )

