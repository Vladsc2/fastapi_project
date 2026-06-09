from random import randint

def is_taken(chance: float) -> bool:
    value = randint(1, 100)
    if value <= chance:
        return True
    return False


