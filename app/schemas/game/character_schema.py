from typing import Annotated
from app.schemas.base import BaseSchema

class BaseCharacterSchema( BaseSchema ):
    name: str

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name})"



class InputCharacterSchema( BaseCharacterSchema ):
    pass



class FullBaseCharacterSchema( BaseCharacterSchema ):
    id: int
    lvl: int = 1

    hp: int = 9
    mana: int = 0

    prepared_spell_1_id: int | None = None
    prepared_spell_2_id: int | None = None
    prepared_spell_3_id: int | None = None
    prepared_spell_4_id: int | None = None
    prepared_spell_5_id: int | None = None
    prepared_spell_6_id: int | None = None
    available_spells: int = 0

    stat_strength: int = 7
    stat_dexterity: int = 7
    stat_constitution: int = 7
    stat_intelligence: int = 7
    stat_will: int = 7


    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, lvl={self.lvl})"



class MobSchema( FullBaseCharacterSchema ):
    desc: str = ""



class MainCharacterSchema( FullBaseCharacterSchema ):
    game_id: int | None = None

    energy: float = 5
    energy_per_minute: float = 0.06


    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, lvl={self.lvl}), hp={self.hp}, energy={self.energy}"