from random import randint, shuffle
from game_data import const


def roll_by_const(roll_const: str) -> int:
    if roll_const == const.Roll.ROLL_2:
        return roll2()
    elif roll_const == const.Roll.ROLL_4:
        return roll4()
    elif roll_const == const.Roll.ROLL_6:
        return roll6()
    elif roll_const == const.Roll.ROLL_8:
        return roll8()
    elif roll_const == const.Roll.ROLL_10:
        return roll10()
    elif roll_const == const.Roll.ROLL_12:
        return roll12()
    elif roll_const == const.Roll.ROLL_20:
        return roll20()
    elif roll_const == const.Roll.ROLL_PERCENT:
        return roll_percent()
    return 0


def roll2() -> int:
    return randint(1, 2)


def roll4() -> int:
    return randint(1, 4)


def roll6() -> int:
    return randint(1, 6)


def roll8() -> int:
    return randint(1, 8)


def roll10() -> int:
    return randint(1, 10)


def roll12() -> int:
    return randint(1, 12)


def roll20() -> int:
    return randint(1, 20)


def roll_percent() -> int:
    percents = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    shuffle( percents )
    return percents[0]