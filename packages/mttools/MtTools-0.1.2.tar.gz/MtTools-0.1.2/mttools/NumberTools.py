import numpy as np


def perfect_factors(n):
    """
    Generates perfect factors of number starting with 1

    :param n: (int)
        number to find the factors of
    :yields: (int)
        next factor
    """
    # "1" is always a divisor
    yield 1
    # likewise n is always a divisor
    yield n

    largest = int(np.sqrt(n))

    # special-case square numbers to avoid yielding the same divisor twice
    if largest * largest == n:
        yield largest
    else:
        largest += 1

    # all other divisors
    for i in range(2, largest):
        if n % i == 0:
            yield i
            yield n / i
