

def get_genitive_turn_word(turn: int) -> str:
    if turn in [1]:
        return "ход"
    elif turn in [2, 3, 4]:
        return "хода"
    else:
        return "ходов"