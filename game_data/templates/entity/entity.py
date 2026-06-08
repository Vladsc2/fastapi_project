from dataclasses import dataclass, field

@dataclass
class DropSpec():
    url: str
    quantity: int
    chance: float

    # Если True:
    #    Пройтись по range(quantity) и определить выпадение каждого отдельного предмета по шансу chance (0-quantity)
    # Если False:
    #    Определить выпадение всех предметов разом (то есть с шансом `chance` выпадет либо `quantity` предметов, либо 0)
    single_mode: bool = False



@dataclass
class BaseEntityGS():
    name: str = "Entity"
    description: str = ""

    lvl: int = 1

    min_hp: int = 5
    max_hp: int = 5

    min_mana: int = 0
    max_mana: int = 0

    actions: int = 1
    actions_max: int = 1
    bonus_actions: int = 1
    bonus_actions_max: int = 1

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

    # list[EffectApplication]
    effects: list = field(default_factory=list)

    weapon_url: str = ""

    # list[DropSpec]
    exp: float = 0
    loot: list = field(default_factory=list)