from app.schemas.base import BaseSchema
from game_data import const


class ScriptSchema( BaseSchema ):
    trigger: str
    url: str
    only_one: bool