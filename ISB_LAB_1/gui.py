import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from typing import Dict

from file_utils import read_json_from_file

class CryptoGUI:
    """Графический интерфейс для шифра Виженера и частотного анализа."""

    def __init__(self, root: tk.Tk, settings_path: str = "settings.json"):
        """
        Инициализирует графический интерфейс с настройками.

        Args:
            root: Корневое окно Tkinter.
            settings_path: Путь к JSON-файлу с настройками. По умолчанию 'settings.json'.
        """
        self.root = root
        self.root.title("Crypto GUI")
        self.root.geometry("400x300")
        self.settings = read_json_from_file(settings_path)

        # Секция шифра Виженера
        self.vigenere_frame = tk.LabelFrame(
            root, text="Шифр Виженера (Часть 1)", padx=10, pady=10
        )
        self.vigenere_frame.pack(padx=10, pady=5, fill="x")
        tk.Button(
            self.vigenere_frame,
            text="Проверить наличие файлов",
            command=lambda: self.check_files("vigenere")
        ).pack(pady=5)
        tk.Button(
            self.vigenere_frame,
            text="Запустить шифрование Виженера",
            command=lambda: self.run_script("vigenere", mode="encrypt")
        ).pack(pady=5)
        tk.Button(
            self.vigenere_frame,
            text="Запустить расшифровку Виженера",
            command=lambda: self.run_script("vigenere", mode="decrypt")
        ).pack(pady=5)

        # Секция частотного анализа
        self.freq_frame = tk.LabelFrame(
            root, text="Частотный анализ (Часть 2)", padx=10, pady=10
        )
        self.freq_frame.pack(padx=10, pady=5, fill="x")
        tk.Button(
            self.freq_frame,
            text="Проверить наличие файлов",
            command=lambda: self.check_files("frequency")
        ).pack(pady=5)
        tk.Button(
            self.freq_frame,
            text="Запустить частотный анализ",
            command=lambda: self.run_script("frequency")
        ).pack(pady=5)

    def check_files(self, script_type: str) -> None:
        """
        Проверяет наличие необходимых файлов для указанного типа скрипта.

        Args:
            script_type: Тип скрипта ('vigenere' или 'frequency').
        """
        config = self.settings[script_type]
        base_dir = config["base_dir"]
        required_files = config["required_files"]
        missing_files = []

        for logical_name, file_name in required_files.items():
            file_path = Path(base_dir) / file_name
            if not file_path.exists():
                missing_files.append(f"{logical_name} ({file_path})")

        if missing_files:
            messagebox.showwarning(
                "Отсутствуют файлы",
                "Убедитесь, что существуют:\n" + "\n".join(missing_files)
            )
        else:
            messagebox.showinfo("Проверка файлов", "Все необходимые файлы на месте!")

    def run_script(self, script_type: str, mode: str = "encrypt") -> None:
        """
        Запускает скрипт на основе настроек.

        Args:
            script_type: Тип скрипта для запуска ('vigenere' или 'frequency').
            mode: Режим для Виженера ('encrypt' или 'decrypt'). По умолчанию 'encrypt'.
        """
        config = self.settings[script_type]
        base_dir = Path(config["base_dir"]).resolve()  # Убедитесь, что путь разрешен
        script = config["script"]
        required_files = config["required_files"]

        # Проверяем наличие всех необходимых файлов
        for logical_name, file_name in required_files.items():
            file_path = base_dir / file_name
            if not file_path.exists():
                messagebox.showerror("Ошибка", f"Отсутствует файл: {logical_name} ({file_path})")
                return

        try:
            match script_type:
                case "vigenere":
                    input_file = (
                        self.settings["general"]["input_file"]
                        if mode == "encrypt"
                        else "new_text.txt"
                    )
                    output_file = (
                        config["output_file"]
                        if mode == "encrypt"
                        else "decrypted_text.txt"
                    )
                    cmd = [
                        "python", script,
                        "--input", base_dir / input_file,
                        "--key", base_dir / self.settings["general"]["key_file"],
                        "--output", base_dir / output_file,
                        "--mode", mode
                    ]
                    success_msg = (
                        config["success_message_template"].format(
                            output_file=base_dir / output_file
                        )
                        if mode == "encrypt"
                        else (
                            f"Расшифровка Виженера успешно завершена!\n"
                            f"Проверьте {base_dir / output_file}"
                        )
                    )
                case "frequency":
                    alphabet_path = base_dir / self.settings["general"]["alphabet_probabilities_file"]
                    cmd = [
                        "python", script,
                        "--encrypted", base_dir / self.settings["general"]["encrypted_text_file"],
                        "--alphabet", alphabet_path,
                        "--output-preliminary", base_dir / config["output_files"]["preliminary_code_file"],
                        "--output-probabilities", base_dir / config["output_files"]["probabilities_file"]
                    ]
                    success_msg = config["success_message_template"].format(
                        preliminary_code_file=base_dir / config["output_files"]["preliminary_code_file"],
                        probabilities_file=base_dir / config["output_files"]["probabilities_file"]
                    )
                case _:
                    raise ValueError(f"Неизвестный тип скрипта: {script_type}")

            subprocess.run(
                cmd, cwd=base_dir, capture_output=True, text=True, check=True
            )
            messagebox.showinfo("Успех", success_msg)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Ошибка", f"Ошибка выполнения:\n{e.stderr}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

def main() -> None:
    """Запускает приложение с графическим интерфейсом."""
    root = tk.Tk()
    app = CryptoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
