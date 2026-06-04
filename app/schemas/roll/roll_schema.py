from pydantic import BaseModel, Field
from typing import Literal


class RollSchema(BaseModel):
    dice: Literal["2", "4", "6", "8", "10", "12", "20", "percent"]



class RollSchemaTimes( RollSchema ):
    times: int = Field(..., ge=1, le=10, description="Кол-во бросков кубика")