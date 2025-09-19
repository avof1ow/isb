import json
import sys

def read_text_from_file(file_path: str) -> str:
    """Читает текст из файла с обработкой исключений."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.")
        sys.exit(1)
    except PermissionError:
        print(f"Ошибка: Нет прав на чтение файла {file_path}.")
        sys.exit(1)
    except Exception as e:
        print(f"Произошла ошибка при чтении файла {file_path}: {e}")
        sys.exit(1)

def write_text_to_file(file_path: str, text: str) -> None:
    """Записывает текст в файл с обработкой исключений."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
    except PermissionError:
        print(f"Ошибка: Нет прав на запись в файл {file_path}.")
        sys.exit(1)
    except Exception as e:
        print(f"Произошла ошибка при записи в файл {file_path}: {e}")
        sys.exit(1)

def read_json_from_file(file_path: str) -> dict:
    """Читает JSON из файла с обработкой исключений."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.")
        sys.exit(1)
    except PermissionError:
        print(f"Ошибка: Нет прав на чтение файла {file_path}.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Ошибка: Файл {file_path} не является допустимым JSON.")
        sys.exit(1)
    except Exception as e:
        print(f"Произошла ошибка при чтении JSON из {file_path}: {e}")
        sys.exit(1)

def read_key_from_json(file_path: str) -> str:
    """Читает ключ из JSON-файла с обработкой исключений."""
    try:
        data = read_json_from_file(file_path)
        return data['key']
    except KeyError:
        print(f"Ошибка: В файле {file_path} отсутствует поле 'key'.")
        sys.exit(1)

def load_settings(settings_path: str) -> dict:
    """Загружает настройки из JSON-файла."""
    return read_json_from_file(settings_path)

def write_json_to_file(file_path: str, data: dict) -> None:
    """Записывает данные в JSON-файл с обработкой исключений."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)
    except PermissionError:
        print(f"Ошибка: Нет прав на запись в файл {file_path}.")
        sys.exit(1)
    except Exception as e:
        print(f"Произошла ошибка при записи JSON в {file_path}: {e}")
        sys.exit(1)
        
        