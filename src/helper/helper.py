import math
from typing import List


def compute_quantile(pool: List[float], percentile: float) -> float:
    pool.sort()
    n = len(pool)
    if n == 1:
        return pool[0]
    else:
        if 0 < percentile <= 100:
            quantile = percentile / 100
            pos = quantile * (n + 1)
            if pos < 1:
                return pool[0]
            if math.floor(pos) >= (n - 1):
                return pool[n - 1]
            dif = pos - math.floor(pos)
            if dif == 0:
                return pool[int(pos) - 1]
            else:
                return pool[math.floor(pos) - 1] + dif * (pool[math.floor(pos)] - pool[math.floor(pos) - 1])
        elif percentile <= 0 or percentile > 100:
            raise ValueError("Percentile is out of range")
