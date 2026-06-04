from dataclasses import dataclass
from game_data.const import const_modifier
from game_data import const

@dataclass
class EffectApplication():
    url: str
    time: int



class BaseEffect():
    # system
    _category = "effect"
    _effect_type: str

    _meta: dict

    def _form_effect_meta(
            self,
            game_model,
            room_model,
            player_char,
            caster,
            target,
    ):
        self._meta = {
            self.Meta.GAME_MODEL: game_model,
            self.Meta.ROOM_MODEL: room_model,
            self.Meta.PLAYER_CHAR: player_char,
            self.Meta.CASTER: caster,
            self.Meta.TARGET: target,
        }


    # const
    class Type:
        TICK_EFFECT = "Tick"
        STAT_MODIFIER = "Stat modifier"


    class Alignment:
        POSITIVE = "Positive"
        NEGATIVE = "Negative"
        NEUTRAL = "Neutral"


    class Meta:
        GAME_MODEL = 0
        ROOM_MODEL = 1
        PLAYER_CHAR = 2
        CASTER = 3
        TARGET = 4


    # interface
    def meta(self, const: int, default=None):
        return self._meta.get(const, default)


    # override
    id: str
    event: str = const.Event.START_TURN
    updatable: bool = False
    alignment: str




class TickEffect( BaseEffect ):
    # system
    _category = BaseEffect._category + "/tick"
    _effect_type = BaseEffect.Type.TICK_EFFECT

    # override
    # id: str
    # event: str = const.Event.START_TURN
    # updatable: bool = False

    name: str
    desc: str

    # const.Stat
    save_throw_stat: str | None = None
    save_throw_diff: int = 10
    alignment: str = BaseEffect.Alignment.NEUTRAL

    def tick(self) -> str:
        return f"Вызван tick() для эффекта '{self.__name__}'\n"


class StatModifierEffect( BaseEffect ):
    # system
    _category = BaseEffect._category + "/stat"
    _effect_type = BaseEffect.Type.STAT_MODIFIER

    # override
    # id: str
    # event: str = const.Event.START_TURN
    # updatable: bool = False
    # alignment: str = BaseEffect.Alignment.NEUTRAL

    # dict[const.Stat, modifier]
    stats: dict[str, int]



def get_stat_modifier_effect_view(effect: type[StatModifierEffect]) -> str:
    text = ""
    for stat_const, stat_value in effect.stats.items():
        text += f"{const_modifier.get_readable_stat(stat_const)} "
        if stat_value > 0:
            text += "+"
        text += f"{stat_value}, "
    text = text[:-2]
    return text