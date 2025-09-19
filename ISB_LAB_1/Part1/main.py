import sys
import argparse
import os
from pathlib import Path

# Настраиваем путь к корню проекта, чтобы найти file_utils.py и settings.json
project_root = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from file_utils import read_json_from_file, read_text_from_file, write_text_to_file

class VigenereCipher:
    """Класс для шифрования и дешифрования текста с использованием шифра Виженера."""

    def __init__(self, alphabet: str):
        self.alphabet = alphabet

    def validate_key(self, key: str) -> None:
        """Проверяет ключ на корректность."""
        if not key or not all(c in self.alphabet for c in key):
            raise ValueError("Ключ должен быть непустым и содержать только символы алфавита")

    def encrypt(self, text: str, key: str) -> str:
        """Шифрует текст с использованием шифра Виженера."""
        self.validate_key(key)
        encrypted_text = ''
        key = key.lower()
        key_index = 0

        for char in text.lower():
            match char:
                case char if char in self.alphabet:
                    char_pos = self.alphabet.index(char)
                    key_char = key[key_index % len(key)]
                    key_pos = self.alphabet.index(key_char)
                    new_pos = (char_pos + key_pos) % len(self.alphabet)
                    encrypted_text += self.alphabet[new_pos]
                    key_index += 1
                case _:
                    encrypted_text += char
        return encrypted_text

    def decrypt(self, text: str, key: str) -> str:
        """Расшифровывает текст с использованием шифра Виженера."""
        self.validate_key(key)
        decrypted_text = ''
        key = key.lower()
        key_index = 0

        for char in text.lower():
            match char:
                case char if char in self.alphabet:
                    char_pos = self.alphabet.index(char)
                    key_char = key[key_index % len(key)]
                    key_pos = self.alphabet.index(key_char)
                    new_pos = (char_pos - key_pos) % len(self.alphabet)
                    decrypted_text += self.alphabet[new_pos]
                    key_index += 1
                case _:
                    decrypted_text += char
        return decrypted_text

def main() -> None:
    parser = argparse.ArgumentParser(description="Шифрование и расшифровка шифром Виженера")
    parser.add_argument("--input", required=True, help="Путь к входному файлу")
    parser.add_argument("--key", required=True, help="Путь к JSON-файлу с ключом")
    parser.add_argument("--output", required=True, help="Путь к выходному файлу")
    parser.add_argument(
        "--mode",
        choices=["encrypt", "decrypt"],
        required=True,
        help="Режим: encrypt или decrypt"
    )
    args = parser.parse_args()

    settings_path = str(project_root / "settings.json")
    try:
        settings = read_json_from_file(settings_path)
        alphabet = settings["general"]["alphabet"]
        input_text = read_text_from_file(args.input)
        key_data = read_json_from_file(args.key)
        key = key_data['key']

        cipher = VigenereCipher(alphabet)

        match args.mode:
            case "encrypt":
                output_text = cipher.encrypt(input_text, key)
            case "decrypt":
                output_text = cipher.decrypt(input_text, key)
            case _:
                raise ValueError("Указан неверный режим")

        write_text_to_file(args.output, output_text)
        print(f"Операция завершена. Результат сохранен в {args.output}")
    except (ValueError, FileNotFoundError, IOError, KeyError) as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
