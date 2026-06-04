from app.schemas.base import BaseSchema
from app.schemas.game.game_schema import GameSchema
from app.schemas.game.character_schema import MainCharacterSchema
from pydantic import Field

class GameAndCharSchema( BaseSchema ):

    game: GameSchema
    main_character: MainCharacterSchema


class CreateGameSchema( BaseSchema ):

    game_slot: int = Field(..., ge=1, le=3)
    character_name: str


class GameSlotSchema( BaseSchema ):

    game_slot: int = Field(..., ge=1, le=3)

