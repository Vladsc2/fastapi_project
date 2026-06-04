

class DamageType():

    class Weapon:
        # Удары тупым предметом: дубины, молоты, падение с высоты, камни
        BLUDGEONING = "Bludgeoning"
        # Проникающие ранения: кинжалы, стрелы, копья, укусы
        PIERCING = "Piercing"
        # Рассекающие удары: мечи, топоры, когти
        SLASHING = "Slashing"


    class Elemental:
        FIRE = "Fire"
        ACID = "Acid"
        COLD = "Cold"
        LIGHTNING = "Lightning"
        THUNDER = "Thunder"


    class Exotic:
        # Иссушение жизни: Луч слабости, прикосновение нежити
        NECROTIC = "Necrotic"
        # Свет и святость: Поражающий удар паладина, кара небес
        RADIANT = "Radiant"
        # Атака на разум: телепатические атаки, заклинания очарования
        PSYCHIC = "Psychic"
        # Чистая магическая энергия: Волшебная стрела. Почти ни у кого нет к нему иммунитета
        FORCE = "Force"
        # Токсины: укусы пауков, ядовитые облака. Самый «слабый» тип
        POISON = "Poison"