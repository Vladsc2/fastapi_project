from app.schemas.base import BaseSchema
from game_data import const


class EffectSchema( BaseSchema ):

    effect_type: str
    event: str
    times: int
    caster_id: int | None    # Если None, то владелец - игрок
    effect_url: str
    value_1: int
    value_2: int
    value_3: int
    value_4: int