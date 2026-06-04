from typing import Annotated
from annotated_types import MinLen, MaxLen
from app.schemas.base import BaseSchema


class ProfilePasswordSchema( BaseSchema ):

    password: Annotated[str, MinLen(6), MaxLen(100)]


class ProfileBaseSchema( BaseSchema ):

    name: Annotated[str, MinLen(3), MaxLen(30)]


    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name})"



class ProfileInputSchema( ProfileBaseSchema ):
    password: Annotated[str, MinLen(6), MaxLen(100)]



class ProfileOutputSchema( ProfileBaseSchema ):
    id: int

    last_ip: str

    first_game_id: int | None
    second_game_id: int | None
    third_game_id: int | None

    active_game_id: int | None

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"



class ProfileFullSchema( ProfileOutputSchema ):
    password: Annotated[str, MinLen(6), MaxLen(100)]