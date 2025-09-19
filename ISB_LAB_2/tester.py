import os
from typing import Optional
from tests import frequency_test, runs_test, longest_run_test

def test_sequence(filename: str) -> Optional[None]:
    """
    Проводит серию тестов для двоичной последовательности.

    Args:
        filename: Путь к файлу, содержащему тестируемую двоичную последовательность.
    """
    if not os.path.exists(filename):
        print(f"Ошибка: Не удалось открыть файл {filename}!")
        return

    with open(filename, 'r') as f:
        sequence = f.readline().strip()

    print(f"\nТестирование последовательности из файла {filename}:")
    print(f"Последовательность: {sequence}")
    print(f"Длина: {len(sequence)}")

    # Выполнение тестов
    p1 = frequency_test(sequence)
    p2 = runs_test(sequence)
    p3 = longest_run_test(sequence)

    # Вывод результатов
    print(f"\nРезультаты тестов для {filename}:")
    print(f"Частотный тест p-значение: {p1:.6f} {'(Passed)' if p1 >= 0.01 else '(Failed)'}")
    print(f"Тест на серии p-значение: {p2:.6f} {'(Passed)' if p2 >= 0.01 else '(Failed)'}")
    print(f"Тест на самую длинную серию p-значение: {p3:.6f} {'(Passed)' if p3 >= 0.01 else '(Failed)'}")