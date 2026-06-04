from typing import TYPE_CHECKING
from app.models.base import BaseModel, BaseIdModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.general import ProfileModel

class IpAssociationsModel( BaseIdModel ):
    __tablename__ = "ip_associations"

    ip_address: Mapped[str] = mapped_column(unique=True)
    profile_id: Mapped[int | None] = mapped_column(ForeignKey("profiles.id", ondelete="CASCADE"))

    profile: Mapped["ProfileModel"] = relationship(back_populates="ip_associations")
