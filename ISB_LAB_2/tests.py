import math
from typing import Tuple, List
from scipy import special

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
    for bit in sequence:
        sum_bits += 1 if bit == '1' else -1

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

    runs = 1  
    for i in range(1, n):
        if sequence[i] != sequence[i-1]:
            runs += 1

    # Вычисление статистики
    mean = (2.0 * ones * (n - ones)) / n + 1
    variance = (2.0 * ones * (n - ones) * (2.0 * ones * (n - ones) - n)) / (n * n * (n - 1))
    z = abs((runs - mean) / math.sqrt(variance))

    p_value = math.erfc(z / math.sqrt(2.0))
    return p_value

def longest_run_test(sequence: str) -> float:
    """
    Проводит тест на самую длинную серию единиц в двоичной последовательности.
    Args:
        sequence: Строка из двоичных цифр ('0' и '1') для тестирования.
    Return:
        p-значение теста.
    """
    #значение из методички
    pi_values = [0.2148, 0.3672, 0.2305, 0.1875]  
    
    length = len(sequence)
    m = 8
    N = 16  

    if length < m * N:
        raise ValueError("Sequence is too short for the test")

    v = [0, 0, 0, 0]

    for i in range(0, m * N, m): 
        block = sequence[i:i + m]
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

    xi_square = sum(((v[i] - N * pi_values[i]) ** 2) / (N * pi_values[i]) for i in range(4))
    
    p_value = special.gammainc(3/2, xi_square/2)
    
    return p_value