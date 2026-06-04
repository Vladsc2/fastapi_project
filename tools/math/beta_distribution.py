import random

def randint_beta(low: int, high: int, mode: float, k: float = 2.0) -> int:
    """
    k >= 0.  Чем больше k, тем сильнее стягивание к mode.
    k = 0 -> равномерное распределение.
    """
    if low == high:
        return low
    if low != high and mode == 0 and low != 0:
        mode = (high + low) / 2

    norm_mode = (mode - low) / (high - low)
    alpha = 1 + norm_mode * k
    beta = 1 + (1 - norm_mode) * k
    if alpha <= 0 or beta <= 0:
        raise ValueError("Слишком маленькое k")
    b = random.betavariate(alpha, beta)
    return int(round(low + b * (high - low)))



def randfloat_beta(low: float, high: float, mode: float, k: float = 2.0) -> float:
    """
    k >= 0.  Чем больше k, тем сильнее стягивание к mode.
    k = 0 -> равномерное распределение.
    """
    if low == high:
        return low
    if low != high and mode == 0 and low != 0:
        mode = (high + low) / 2

    norm_mode = (mode - low) / (high - low)
    alpha = 1 + norm_mode * k
    beta = 1 + (1 - norm_mode) * k
    if alpha <= 0 or beta <= 0:
        raise ValueError("Слишком маленькое k")
    b = random.betavariate(alpha, beta)
    return float(low + b * (high - low))

