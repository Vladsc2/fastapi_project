from app.schemas.base import BaseSchema

class GameSchema( BaseSchema ):

    character_id: int | None = None

    major_state: str | None = None
    world_id: int | None = None
    raid_id: int | None = None
    room_id: int | None = None

    meta_id: int | None = None


    def __repr__(self):
        return f"{self.__class__.__name__}(character_id={self.character_id}, major_state_id={self.major_state_id})"

