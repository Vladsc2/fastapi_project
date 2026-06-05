from dataclasses import dataclass
from game_data.const import const_modifier
from game_data import const
from app.schemas.effect import EffectSchema

@dataclass
class EffectApplication():
    url: str
    time: int

    ignore_save_throw: bool = False

    value_1: int = 0
    value_2: int = 0
    value_3: int = 0
    value_4: int = 0



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
            value_1,
            value_2,
            value_3,
            value_4,
    ):
        self._meta = {
            self.Meta.GAME_MODEL: game_model,
            self.Meta.ROOM_MODEL: room_model,
            self.Meta.PLAYER_CHAR: player_char,
            self.Meta.CASTER: caster,
            self.Meta.TARGET: target,
            self.Meta.VALUE_1: value_1,
            self.Meta.VALUE_2: value_2,
            self.Meta.VALUE_3: value_3,
            self.Meta.VALUE_4: value_4,
        }


    # override
    def view(self, value_1: int, value_2: int, value_3: int, value_4: int) -> str:
        return ""


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

        VALUE_1 = 5
        VALUE_2 = 6
        VALUE_3 = 7
        VALUE_4 = 8


    # interface
    def meta(self, meta_const: int, default=None):
        return self._meta.get(meta_const, default)


    # override
    id: str
    event: str = const.Event.START_TURN
    updatable: bool = False
    alignment: str

    # const.Stat
    save_throw_stat: str | None = None
    save_throw_diff: int = 10




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

    alignment: str = BaseEffect.Alignment.NEUTRAL

    def tick(self) -> str:
        return f"Вызван tick() для эффекта '{self.__name__}'\n"


class StatModifierEffect( BaseEffect ):
    # system
    _category = BaseEffect._category + "/stat"
    _effect_type = BaseEffect.Type.STAT_MODIFIER

    # override
    # id: str
    event: str = const.Event.END_TURN
    # updatable: bool = False
    alignment: str = BaseEffect.Alignment.NEUTRAL

    # -> dict[const.Stat, modifier]
    @staticmethod
    def get_stats_modifiers(
            value_1: int,
            value_2: int,
            value_3: int,
            value_4: int,
    ) -> dict[str, int]:
        return {}



def get_stat_modifier_effect_view(
        effect: type[StatModifierEffect],
        effect_schema: EffectSchema
) -> str:
    text = ""
    stat_dict = effect.get_stats_modifiers(
            value_1=effect_schema.value_1,
            value_2=effect_schema.value_2,
            value_3=effect_schema.value_3,
            value_4=effect_schema.value_4
        )
    for stat_const, stat_value in stat_dict.items():
        text += f"{const_modifier.get_readable_stat(stat_const)} "
        if stat_value > 0:
            text += "+"
        text += f"{stat_value}, "
    text = text[:-2]
    return text