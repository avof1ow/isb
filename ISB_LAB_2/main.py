import json
from typing import Dict, Any, Tuple
from tester import test_sequence


def read_sequence(filename: str) -> str:
    """
    Чтение бинарной последовательности из файла.

    Args:
        filename: Путь к файлу с последовательностью

    Returns:
        Бинарная последовательность в виде строки
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            sequence = f.readline().strip()
        return sequence
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла {filename}: {e}")


def write_to_file(random_gen: str, sequence: str, file_path: str, results: Tuple[float, float, float]) -> None:
    """
    Запись результатов тестов в файл.

    Args:
        random_gen: название генератора случайных значений
        sequence: тестируемая бинарная последовательность
        file_path: путь к файлу, куда запишем результаты тестов
        results: кортеж с результатами тестов (p1, p2, p3)
    """
    try:
        with open(f'{file_path}', 'a', encoding='utf-8') as file:
            file.write(f"\nРезультаты тестов для {random_gen}:\n")
            file.write(f"Последовательность: {sequence}\n")
            file.write(
                f"Частотный тест p-значение: {results[0]:.6f} {'(Passed)' if results[0] >= 0.01 else '(Failed)'}\n")
            file.write(
                f"Тест на серии p-значение: {results[1]:.6f} {'(Passed)' if results[1] >= 0.01 else '(Failed)'}\n")
            file.write(
                f"Тест на самую длинную серию p-значение: {results[2]:.6f} {'(Passed)' if results[2] >= 0.01 else '(Failed)'}\n")
            file.write("-" * 60 + "\n\n")
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} отсутствует")
    except Exception as ex:
        raise Exception(f"Ошибка при записи в файл: {ex}")


def main() -> int:
    """
    Главная функция программы.
    Считываются данные конфигурационного файла и запускается тестирование.

    Returns:
        0 в случае успешного выполнения, 1 при возникновении ошибок.
    """
    # Чтение settings.json
    try:
        with open("settings.json", 'r') as config_file:
            config: Dict[str, Any] = json.load(config_file)
    except FileNotFoundError:
        print("Ошибка: Не удалось открыть файл settings.json!")
        return 1
    except json.JSONDecodeError as e:
        print(f"Ошибка: Не удалось разобрать settings.json: {e}")
        return 1

    # Получение путей к файлам
    try:
        cpp_input_file: str = config["input_file_cpp"]
        java_input_file: str = config["input_file_java"]
        results_file: str = config["results"]
    except KeyError as e:
        print(f"Ошибка: В settings.json отсутствует ключ '{e}'!")
        return 1

    # Тестирование последовательностей и запись результатов
    try:
        # Чтение и тестирование C++ последовательности
        cpp_sequence = read_sequence(cpp_input_file)
        cpp_results = test_sequence(cpp_input_file)
        write_to_file("C++ Генератор", cpp_sequence, results_file, cpp_results)

        # Чтение и тестирование Java последовательности
        java_sequence = read_sequence(java_input_file)
        java_results = test_sequence(java_input_file)
        write_to_file("Java Генератор", java_sequence, results_file, java_results)

    except Exception as e:
        print(f"Ошибка во время тестирования: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
