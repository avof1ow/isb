from tests import frequency_test, runs_test, longest_run_test


def test_sequence(filename: str) -> tuple[float, float, float]:
    """
    Проводит серию тестов для двоичной последовательности.

    Args:
        filename: Путь к файлу, содержащему тестируемую двоичную последовательность.
    Return:
        tuple(float, float, float): Кортеж, состоящий из результатов тестов
    """

    with open(filename, 'r') as f:
        sequence = f.readline().strip()

    # Выполнение тестов
    p1 = frequency_test(sequence)
    p2 = runs_test(sequence)
    p3 = longest_run_test(sequence)

    return p1, p2, p3
