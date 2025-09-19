import os
import sys
import argparse
from collections import Counter
from pathlib import Path
from typing import Dict
import json

def setup_project_path() -> None:
    """Настраивает путь к корню проекта для импорта модулей."""
    settings_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "settings.json"
    )
    if os.path.exists(settings_path):
        with open(settings_path, 'r', encoding='utf-8') as file:
            settings = json.load(file)
            project_root = Path(os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    settings["project_root"]
                )
            ))
            if str(project_root) not in sys.path:
                sys.path.insert(0, str(project_root))

setup_project_path()

from file_utils import read_json_from_file, write_json_to_file, read_text_from_file, write_text_to_file

def frequency_analysis(text: str) -> Dict[str, float]:
    """
    Выполняет частотный анализ текста.

    Args:
        text: Текст для анализа.

    Returns:
        Словарь с вероятностями появления символов.

    Raises:
        ValueError: Если входной текст пустой.
    """
    if not text:
        raise ValueError("Входной текст не может быть пустым")
    text = text.replace('\n', '')
    total_chars = len(text)
    char_count = Counter(text)
    return {char: count / total_chars for char, count in char_count.items()}

def write_probabilities(probabilities: Dict[str, float], file_path: str) -> None:
    """
    Записывает вероятности символов в JSON-файл.

    Args:
        probabilities: Словарь с вероятностями символов.
        file_path: Путь к выходному файлу.

    Raises:
        IOError: Если запись в файл невозможна.
    """
    try:
        write_json_to_file(file_path, probabilities)
    except IOError as e:
        raise IOError(f"Не удалось записать вероятности в {file_path}: {e}")

def read_alphabet_probs(file_path: str) -> Dict[str, float]:
    """
    Читает вероятности алфавита из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу с вероятностями алфавита.

    Returns:
        Словарь с вероятностями символов алфавита.

    Raises:
        FileNotFoundError: Если файл не найден.
        json.JSONDecodeError: Если содержимое файла некорректно.
    """
    try:
        data = read_json_from_file(file_path)
        return {char: float(prob) for char, prob in data.items()}
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise type(e)(f"Ошибка чтения вероятностей алфавита из {file_path}: {e}")

def create_substitution(
        encrypted_probs: Dict[str, float],
        alphabet_probs: Dict[str, float]
) -> Dict[str, str]:
    """
    Создает словарь замены символов на основе отсортированных вероятностей.

    Args:
        encrypted_probs: Вероятности зашифрованного текста.
        alphabet_probs: Вероятности алфавита.

    Returns:
        Словарь, отображающий зашифрованные символы на символы алфавита.
    """
    encrypted_sorted = sorted(encrypted_probs.items(), key=lambda x: x[1], reverse=True)
    alphabet_sorted = sorted(alphabet_probs.items(), key=lambda x: x[1], reverse=True)
    return {
        enc_char: alpha_char
        for (enc_char, _), (alpha_char, _) in zip(encrypted_sorted, alphabet_sorted)
    }

def decrypt_text(encrypted_text: str, substitution: Dict[str, str]) -> str:
    """
    Расшифровывает текст с использованием словаря замены.

    Args:
        encrypted_text: Зашифрованный текст.
        substitution: Словарь для замены зашифрованных символов на открытые.

    Returns:
        Расшифрованный текст.
    """
    return ''.join(substitution.get(char, char) for char in encrypted_text)

def main() -> None:
    parser = argparse.ArgumentParser(description="Частотный анализ и расшифровка")
    parser.add_argument(
        "--encrypted",
        required=True,
        help="Путь к файлу с зашифрованным текстом"
    )
    parser.add_argument(
        "--alphabet",
        required=True,
        help="Путь к JSON-файлу с вероятностями алфавита"
    )
    parser.add_argument(
        "--output-preliminary",
        required=True,
        help="Путь к файлу с предварительной расшифровкой"
    )
    parser.add_argument(
        "--output-probabilities",
        required=True,
        help="Путь к файлу с вероятностями"
    )
    args = parser.parse_args()

    try:
        encrypted_text = read_text_from_file(args.encrypted)
        probabilities = frequency_analysis(encrypted_text)
        write_probabilities(probabilities, args.output_probabilities)
        alphabet_probabilities = read_alphabet_probs(args.alphabet)
        substitution = create_substitution(probabilities, alphabet_probabilities)
        decrypted_text = decrypt_text(encrypted_text, substitution)
        write_text_to_file(args.output_preliminary, decrypted_text)
        print("Частотный анализ и расшифровка завершены.")
    except (ValueError, IOError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
