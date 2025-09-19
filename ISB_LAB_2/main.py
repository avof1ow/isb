import json
from typing import Dict, Any
from tester import test_sequence

def main() -> int:
    """
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

    # Получение путей к входным файлам
    try:
        cpp_input_file: str = config["input_file_cpp"]
        java_input_file: str = config["input_file_java"]
    except KeyError as e:
        print(f"Ошибка: В settings.json отсутствует ключ '{e}'!")
        return 1

    # Тестирование последовательностей
    test_sequence(cpp_input_file)
    test_sequence(java_input_file)

    return 0

if __name__ == "__main__":
    exit(main())