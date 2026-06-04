from game_data import const

def get_readable_dice_name(roll_const: str) -> str:
    if roll_const == const.Roll.ROLL_2:
        return "d2"
    elif roll_const == const.Roll.ROLL_4:
        return "d4"
    elif roll_const == const.Roll.ROLL_6:
        return "d6"
    elif roll_const == const.Roll.ROLL_8:
        return "d8"
    elif roll_const == const.Roll.ROLL_10:
        return "d10"
    elif roll_const == const.Roll.ROLL_12:
        return "d12"
    elif roll_const == const.Roll.ROLL_20:
        return "d20"
    elif roll_const == const.Roll.ROLL_PERCENT:
        return "percent dice"

    return const.NONE_CONST



def get_readable_damage_type(damage_type: str) -> str:
    if damage_type == const.DamageType.Weapon.SLASHING:
        return "Режущий"
    if damage_type == const.DamageType.Weapon.PIERCING:
        return "Колющий"
    if damage_type == const.DamageType.Weapon.BLUDGEONING:
        return "Дробящий"


    if damage_type == const.DamageType.Exotic.NECROTIC:
        return "Некротический"
    if damage_type == const.DamageType.Exotic.RADIANT:
        return "Сияющий"
    if damage_type == const.DamageType.Exotic.PSYCHIC:
        return "Психический"
    if damage_type == const.DamageType.Exotic.FORCE:
        return "Силовой"
    if damage_type == const.DamageType.Exotic.POISON:
        return "Отравляющий"

    return const.NONE_CONST


def get_readable_genitive_damage_type(damage_type: str) -> str:
    if damage_type == const.DamageType.Weapon.SLASHING:
        return "Режущего"
    elif damage_type == const.DamageType.Weapon.PIERCING:
        return "Колющего"
    elif damage_type == const.DamageType.Weapon.BLUDGEONING:
        return "Дробящего"


    if damage_type == const.DamageType.Exotic.NECROTIC:
        return "Некротического"
    if damage_type == const.DamageType.Exotic.RADIANT:
        return "Сияющего"
    if damage_type == const.DamageType.Exotic.PSYCHIC:
        return "Психического"
    if damage_type == const.DamageType.Exotic.FORCE:
        return "Силового"
    if damage_type == const.DamageType.Exotic.POISON:
        return "Отравляющего"

    return const.NONE_CONST




def get_readable_stat(stat: str) -> str:
    if stat == const.Stat.Strength:
        return "Сила"
    if stat == const.Stat.Dexterity:
        return "Ловкость"
    if stat == const.Stat.Constitution:
        return "Телосложение"
    if stat == const.Stat.Intelligence:
        return "Интеллект"
    if stat == const.Stat.Will:
        return "Воля"

    return const.NONE_CONST


def get_readable_genitive_stat(stat: str) -> str:
    if stat == const.Stat.Strength:
        return "Силы"
    if stat == const.Stat.Dexterity:
        return "Ловкости"
    if stat == const.Stat.Constitution:
        return "Телосложения"
    if stat == const.Stat.Intelligence:
        return "Интеллекта"
    if stat == const.Stat.Will:
        return "Воли"

    return const.NONE_CONST



def target_number_to_target_const(target_number: int) -> str:
    if target_number == 1:
        return const.Stopper.Battle.ENEMY_POINTER_1
    if target_number == 2:
        return const.Stopper.Battle.ENEMY_POINTER_2
    if target_number == 3:
        return const.Stopper.Battle.ENEMY_POINTER_3
    if target_number == 4:
        return const.Stopper.Battle.ENEMY_POINTER_4
    if target_number == 5:
        return const.Stopper.Battle.ENEMY_POINTER_5
    if target_number == 6:
        return const.Stopper.Battle.ENEMY_POINTER_6
    if target_number == 7:
        return const.Stopper.Battle.ENEMY_POINTER_7
    if target_number == 8:
        return const.Stopper.Battle.ENEMY_POINTER_8
    if target_number == 9:
        return const.Stopper.Battle.ENEMY_POINTER_9
    if target_number == 10:
        return const.Stopper.Battle.ENEMY_POINTER_10

    return const.NONE_CONST



def target_const_to_target_number(target_const: str) -> int:
    if target_const == const.Stopper.Battle.ENEMY_POINTER_1:
        return 1
    if target_const == const.Stopper.Battle.ENEMY_POINTER_2:
        return 2
    if target_const == const.Stopper.Battle.ENEMY_POINTER_3:
        return 3
    if target_const == const.Stopper.Battle.ENEMY_POINTER_4:
        return 4
    if target_const == const.Stopper.Battle.ENEMY_POINTER_5:
        return 5
    if target_const == const.Stopper.Battle.ENEMY_POINTER_6:
        return 6
    if target_const == const.Stopper.Battle.ENEMY_POINTER_7:
        return 7
    if target_const == const.Stopper.Battle.ENEMY_POINTER_8:
        return 8
    if target_const == const.Stopper.Battle.ENEMY_POINTER_9:
        return 9
    if target_const == const.Stopper.Battle.ENEMY_POINTER_10:
        return 10