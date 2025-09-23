import math
from scipy import special
from constants import SIZE_BLOCK, PI_VALUES, NUMBER_OF_BLOCKS

def frequency_test(sequence: str) -> float:
    """
    Проводит частотный тест для двоичной последовательности.
    Args:
        sequence: Строка из двоичных цифр ('0' и '1') для тестирования.
    Return:
        p-значение теста.
    """
    n = len(sequence)
    sum_bits = 0

    # Подсчет суммы: +1 для '1', -1 для '0'
    sum_bits = sum( 1 if bit == '1' else -1 for bit in sequence )

    # Вычисление статистики
    s_obs = abs(sum_bits) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2.0))

    return p_value

def runs_test(sequence: str) -> float:
    """
    Проводит тест на количество серий в двоичной последовательности.
    Args:
        sequence: Строка из двоичных цифр ('0' и '1') для тестирования.
    Return:
        0.0, если последовательность слишком смещена для проведения теста.
        p-значение теста.
    """
    n = len(sequence)
    ones = sequence.count('1')

    # Проверка условия: доля единиц близка к 0.5
    pi = ones / n
    if abs(pi - 0.5) >= 2.0 / math.sqrt(n):
        print(f"Тест на серии: Доля единиц ({pi:.6f}) слишком отклоняется. Тест не пройден.")
        return 0.0

    runs = 0
    for i in range(1, n):
        if sequence[i] != sequence[i-1]:
            runs += 1

    # Вычисление статистики
    numerator = abs(runs - 2 * n * ones * (1 - ones))
    denominator = 2 * (math.sqrt(2 * n)) * ones * (1 - ones)

    # Защита от деления на ноль
    if denominator == 0:
        return 0.0

    p_value = math.erfc(numerator / denominator)
    return p_value


def longest_run_test(sequence: str) -> float:
    """
    Проводит тест на самую длинную серию единиц в двоичной последовательности.
    Args:
        sequence: Строка из двоичных цифр ('0' и '1') для тестирования.
    Return:
        p-значение теста.
    """

    length = len(sequence)

    if length < SIZE_BLOCK * NUMBER_OF_BLOCKS:
        raise ValueError("Sequence is too short for the test")

    v = [0, 0, 0, 0]

    for i in range(0, SIZE_BLOCK * NUMBER_OF_BLOCKS, SIZE_BLOCK):
        block = sequence[i:i + SIZE_BLOCK]
        max_length = current = 0

        for bit in block:
            current = current + 1 if bit == '1' else 0
            max_length = max(max_length, current)

        match max_length:
            case max_length if max_length <= 1:
                v[0] += 1
            case 2:
                v[1] += 1
            case 3:
                v[2] += 1
            case max_length if max_length >= 4:
                v[3] += 1

    xi_square = sum(((v[i] - NUMBER_OF_BLOCKS * PI_VALUES[i]) ** 2) / (NUMBER_OF_BLOCKS * PI_VALUES[i]) for i in range(4))
    
    p_value = special.gammaincc(3/2, xi_square/2)
    
    return p_value
