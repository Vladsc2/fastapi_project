from app.models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

class BaseIdModel( BaseModel ):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)