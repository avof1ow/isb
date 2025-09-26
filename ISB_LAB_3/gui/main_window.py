import logging
import time
import tkinter as tk
from tkinter import messagebox
from typing import Optional

import ttkbootstrap as ttk
from ttkbootstrap.constants import DARK, SUCCESS, DANGER, INVERSE, PRIMARY

from core.exceptions import CryptoError, KeyGenerationError, EncryptionError, DecryptionError, FileOperationError
from core.hybrid import generate_rsa_keys, hybrid_encrypt, hybrid_decrypt
from gui.styles import configure_styles
from gui.widgets import PathSelector
from utils.config_manager import ConfigManager
from utils.file_io import read_file, write_file

# Настройка логирования
logger = logging.getLogger(__name__)


class MainWindow(ttk.Window):
    """
    Главное окно приложения Hybrid Crypto System.

    Обеспечивает интерфейс для генерации ключей, шифрования и дешифрования файлов
    с использованием гибридной криптографии (RSA + AES).
    """

    def __init__(self, config_manager: ConfigManager) -> None:
        """
        Инициализирует главное окно приложения.

        Args:
            config_manager: Менеджер конфигурации приложения
        """
        self.config = config_manager
        super().__init__(themename=self.config.get("theme", "darkly"))

        # Настраиваем стили перед созданием интерфейса
        configure_styles(self, self.config)

        self._setup_window()
        self._create_welcome_screen()
        self.after(100, self._animate_welcome_sequence)

    def _setup_window(self) -> None:
        """
        Настраивает основные свойства главного окна.
        """
        self.title("Hybrid Crypto System - RSA + AES")
        self.geometry("900x650")
        self.minsize(800, 550)

        # Дополнительная настройка стилей
        style = ttk.Style()
        style.configure(".", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 11, "bold"))
        style.configure("TLabel", font=("Segoe UI", 11))
        style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=[15, 5])
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("success.TButton", foreground="white")
        style.configure("info.TLabel", foreground="#2ecc71")

    def _create_welcome_screen(self) -> None:
        """
        Создает экран приветствия с анимацией загрузки.
        """
        self.welcome_frame = ttk.Frame(self, bootstyle=DARK)
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)

        # Создаем градиентный фон
        self.canvas = tk.Canvas(self.welcome_frame, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self._create_gradient_background()

        # Контейнер для элементов приветствия
        container = ttk.Frame(self.welcome_frame, bootstyle=DARK)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Логотип и заголовки
        self.logo_label = ttk.Label(
            container,
            text="🔒",
            font=("Segoe UI", 72),
            bootstyle=(SUCCESS, INVERSE),
        )
        self.logo_label.pack(pady=20)

        self.title_label = ttk.Label(
            container,
            text="Hybrid Crypto System",
            font=("Segoe UI", 24, "bold"),
            bootstyle=(SUCCESS, INVERSE),
        )
        self.title_label.pack(pady=10)

        self.subtitle_label = ttk.Label(
            container,
            text="Безопасное шифрование файлов с помощью гибридной криптографии",
            font=("Segoe UI", 12),
            bootstyle=(PRIMARY, INVERSE),
        )
        self.subtitle_label.pack(pady=5)

        # Прогресс-бар загрузки
        self.progress = ttk.Progressbar(
            container,
            mode="determinate",
            maximum=100,
            bootstyle=SUCCESS,
        )
        self.progress.pack(pady=20, fill=tk.X, padx=50)

    def _create_gradient_background(self) -> None:
        """
        Создает градиентный фон на холсте.
        """
        width = self.winfo_width() or 900
        height = self.winfo_height() or 650

        for i in range(height):
            r = int(20 + (i / height) * 30)
            g = int(20 + (i / height) * 50)
            b = int(50 + (i / height) * 70)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, width, i, fill=color)

    def _animate_welcome_sequence(self) -> None:
        """
        Выполняет анимацию экрана приветствия.
        """
        # Анимация прогресс-бара
        for i in range(0, 101, 2):
            self.progress["value"] = i
            self.update()
            time.sleep(0.03)

        # Плавное исчезновение экрана приветствия
        for alpha in range(100, -1, -2):
            self.attributes("-alpha", alpha / 100)
            self.update()
            time.sleep(0.02)

        self.attributes("-alpha", 1.0)
        self.welcome_frame.destroy()
        self._create_main_interface()

    def _create_main_interface(self) -> None:
        """
        Создает основной интерфейс приложения после загрузки.
        """
        self._create_widgets()
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=15, pady=15)

    def _create_widgets(self) -> None:
        """
        Создает основные виджеты интерфейса.
        """
        self.notebook = ttk.Notebook(self, bootstyle=DARK)

        # Создаем вкладки
        self._setup_keygen_tab()
        self._setup_encryption_tab()
        self._setup_decryption_tab()

        # Добавляем вкладки в блокнот
        self.notebook.add(self.key_frame, text="🔑 Генерация ключей")
        self.notebook.add(self.enc_frame, text="🔒 Шифрование")
        self.notebook.add(self.dec_frame, text="🔓 Дешифрование")

        # Создаем строку состояния
        self._create_status_bar()

    def _create_status_bar(self) -> None:
        """
        Создает строку состояния в нижней части окна.
        """
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Frame(self, bootstyle=DARK)
        status_bar.pack(fill=tk.X, padx=5, pady=(0, 5))

        status_label = ttk.Label(
            status_bar,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bootstyle=(SUCCESS, INVERSE),
        )
        status_label.pack(fill=tk.X, expand=True, ipady=3)

    def _setup_keygen_tab(self) -> None:
        """
        Настраивает вкладку генерации ключей.
        """
        self.key_frame = ttk.Frame(self.notebook, padding=15, bootstyle=DARK)

        frame = ttk.Labelframe(
            self.key_frame,
            text="Настройки генерации ключей",
            padding=(15, 10),
        )
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Виджеты выбора путей
        self.priv_key_sel = PathSelector(
            frame,
            "Приватный ключ:",
            [("PEM files", "*.pem")],
            is_save=True,
            initialfile=self.config.get("default_paths.private_key", "private.pem"),
        )

        self.pub_key_sel = PathSelector(
            frame,
            "Публичный ключ:",
            [("PEM files", "*.pem")],
            is_save=True,
            initialfile=self.config.get("default_paths.public_key", "public.pem"),
        )

        self.enc_key_sel = PathSelector(
            frame,
            "Зашифрованный ключ:",
            [("BIN files", "*.bin")],
            is_save=True,
            initialfile=self.config.get("default_paths.encrypted_key", "encrypted_key.bin"),
        )

        # Размещаем виджеты
        for widget in [self.priv_key_sel, self.pub_key_sel, self.enc_key_sel]:
            widget.pack(fill=tk.X, padx=5, pady=8)

        # Кнопка генерации ключей
        btn_frame = ttk.Frame(frame, bootstyle=DARK)
        btn_frame.pack(fill=tk.X, pady=(15, 5))

        ttk.Button(
            btn_frame,
            text="Сгенерировать ключи",
            command=self._generate_keys,
            bootstyle=SUCCESS,
            width=20,
        ).pack(side=tk.LEFT, padx=5)

        # Информационное сообщение
        self._create_info_frame(frame)

    def _setup_encryption_tab(self) -> None:
        """
        Настраивает вкладку шифрования.
        """
        self.enc_frame = ttk.Frame(self.notebook, padding=15, bootstyle=DARK)

        frame = ttk.Labelframe(
            self.enc_frame,
            text="Настройки шифрования",
            padding=(15, 10),
        )
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Виджеты выбора путей
        self.input_enc_sel = PathSelector(
            frame,
            "Файл для шифрования:",
            [("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )

        self.pub_key_enc_sel = PathSelector(
            frame,
            "Публичный ключ:",
            [("PEM files", "*.pem")]
        )

        self.enc_key_enc_sel = PathSelector(
            frame,
            "Зашифрованный ключ:",
            [("BIN files", "*.bin")]
        )

        self.output_enc_sel = PathSelector(
            frame,
            "Выходной файл:",
            [("BIN files", "*.bin")],
            is_save=True,
            initialfile=self.config.get("default_paths.encrypted_file", "encrypted.bin"),
        )

        # Размещаем виджеты
        for widget in [
            self.input_enc_sel,
            self.pub_key_enc_sel,
            self.enc_key_enc_sel,
            self.output_enc_sel,
        ]:
            widget.pack(fill=tk.X, padx=5, pady=8)

        # Кнопка шифрования
        btn_frame = ttk.Frame(frame, bootstyle=DARK)
        btn_frame.pack(fill=tk.X, pady=(15, 5))

        ttk.Button(
            btn_frame,
            text="Зашифровать файл",
            command=self._encrypt_file,
            bootstyle=SUCCESS,
            width=20,
        ).pack(side=tk.LEFT, padx=5)

    def _setup_decryption_tab(self) -> None:
        """
        Настраивает вкладку дешифрования.
        """
        self.dec_frame = ttk.Frame(self.notebook, padding=15, bootstyle=DARK)

        frame = ttk.Labelframe(
            self.dec_frame,
            text="Настройки дешифрования",
            padding=(15, 10),
        )
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Виджеты выбора путей
        self.input_dec_sel = PathSelector(
            frame,
            "Файл для дешифрования:",
            [("BIN files", "*.bin"), ("Все файлы", "*.*")]
        )

        self.priv_key_dec_sel = PathSelector(
            frame,
            "Приватный ключ:",
            [("PEM files", "*.pem")]
        )

        self.enc_key_dec_sel = PathSelector(
            frame,
            "Зашифрованный ключ:",
            [("BIN files", "*.bin")]
        )

        self.output_dec_sel = PathSelector(
            frame,
            "Выходной файл:",
            [("Текстовые файлы", "*.txt")],
            is_save=True,
            initialfile=self.config.get("default_paths.decrypted_file", "decrypted.txt"),
        )

        # Размещаем виджеты
        for widget in [
            self.input_dec_sel,
            self.priv_key_dec_sel,
            self.enc_key_dec_sel,
            self.output_dec_sel,
        ]:
            widget.pack(fill=tk.X, padx=5, pady=8)

        # Кнопка дешифрования
        btn_frame = ttk.Frame(frame, bootstyle=DARK)
        btn_frame.pack(fill=tk.X, pady=(15, 5))

        ttk.Button(
            btn_frame,
            text="Расшифровать файл",
            command=self._decrypt_file,
            bootstyle=SUCCESS,
            width=20,
        ).pack(side=tk.LEFT, padx=5)

    def _create_info_frame(self, parent: ttk.Frame) -> None:
        """
        Создает информационный фрейм с предупреждением.

        Args:
            parent: Родительский виджет
        """
        info_frame = ttk.Frame(parent, bootstyle=DARK)
        info_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Label(
            info_frame,
            text="Предупреждение: Приватный ключ должен быть надёжно сохранён!",
            bootstyle=(DANGER, INVERSE),
            anchor=tk.CENTER,
            padding=5,
        ).pack(fill=tk.X)

    def _generate_keys(self) -> None:
        """
        Генерирует пару RSA-ключей и сохраняет их в файлы.
        """
        try:
            self._update_status("Генерация ключей...", "info")

            keys = generate_rsa_keys()

            # Сохраняем ключи
            priv_key_path = self.priv_key_sel.path or self.config.get("default_paths.private_key")
            pub_key_path = self.pub_key_sel.path or self.config.get("default_paths.public_key")

            write_file(priv_key_path, keys["private_key"])
            write_file(pub_key_path, keys["public_key"])

            logger.info(f"Ключи успешно сгенерированы: {priv_key_path}, {pub_key_path}")
            self._update_status("Ключи успешно сгенерированы!", SUCCESS)
            messagebox.showinfo("Успех", "Ключи успешно сгенерированы!", parent=self)

        except (KeyGenerationError, FileOperationError) as e:
            logger.error(f"Ошибка генерации ключей: {e}")
            self._update_status(f"Ошибка генерации ключей: {e}", DANGER)
            messagebox.showerror("Ошибка", str(e), parent=self)
        except Exception as e:
            logger.error(f"Неожиданная ошибка при генерации ключей: {e}")
            self._update_status("Неожиданная ошибка!", DANGER)
            messagebox.showerror("Ошибка", f"Неожиданная ошибка: {e}", parent=self)

    def _encrypt_file(self) -> None:
        """
        Шифрует выбранный файл с использованием гибридного шифрования.
        """
        try:
            self._update_status("Шифрование файла...", "info")

            # Проверяем обязательные поля
            if not all([self.input_enc_sel.path, self.pub_key_enc_sel.path]):
                raise ValueError("Необходимо указать файл для шифрования и публичный ключ")

            public_key_pem = read_file(self.pub_key_enc_sel.path)
            plaintext = read_file(self.input_enc_sel.path)

            result = hybrid_encrypt(plaintext, public_key_pem)

            # Сохраняем зашифрованные данные
            enc_key_path = self.enc_key_enc_sel.path or self.config.get("default_paths.encrypted_key")
            output_path = self.output_enc_sel.path or self.config.get("default_paths.encrypted_file")

            write_file(enc_key_path, result["encrypted_symmetric"])
            write_file(output_path, result["ciphertext"])

            logger.info(f"Файл успешно зашифрован: {output_path}")
            self._update_status("Шифрование выполнено успешно!", SUCCESS)
            messagebox.showinfo("Успех", "Шифрование выполнено успешно!", parent=self)

        except (EncryptionError, FileOperationError, ValueError) as e:
            logger.error(f"Ошибка шифрования: {e}")
            self._update_status(f"Ошибка шифрования: {e}", DANGER)
            messagebox.showerror("Ошибка", str(e), parent=self)
        except Exception as e:
            logger.error(f"Неожиданная ошибка при шифровании: {e}")
            self._update_status("Неожиданная ошибка!", DANGER)
            messagebox.showerror("Ошибка", f"Неожиданная ошибка: {e}", parent=self)

    def _decrypt_file(self) -> None:
        """
        Дешифрует выбранный файл с использованием гибридного шифрования.
        """
        try:
            self._update_status("Дешифрование файла...", "info")

            # Проверяем обязательные поля
            if not all([self.input_dec_sel.path, self.priv_key_dec_sel.path, self.enc_key_dec_sel.path]):
                raise ValueError("Необходимо указать все обязательные файлы")

            private_key_pem = read_file(self.priv_key_dec_sel.path)
            encrypted_symmetric = read_file(self.enc_key_dec_sel.path)
            ciphertext = read_file(self.input_dec_sel.path)

            plaintext = hybrid_decrypt(ciphertext, encrypted_symmetric, private_key_pem)

            # Сохраняем расшифрованные данные
            output_path = self.output_dec_sel.path or self.config.get("default_paths.decrypted_file")
            write_file(output_path, plaintext)

            logger.info(f"Файл успешно расшифрован: {output_path}")
            self._update_status("Дешифрование выполнено успешно!", SUCCESS)
            messagebox.showinfo("Успех", "Дешифрование выполнено успешно!", parent=self)

        except (DecryptionError, FileOperationError, ValueError) as e:
            logger.error(f"Ошибка дешифрования: {e}")
            self._update_status(f"Ошибка дешифрования: {e}", DANGER)
            messagebox.showerror("Ошибка", str(e), parent=self)
        except Exception as e:
            logger.error(f"Неожиданная ошибка при дешифровании: {e}")
            self._update_status("Неожиданная ошибка!", DANGER)
            messagebox.showerror("Ошибка", f"Неожиданная ошибка: {e}", parent=self)

    def _update_status(self, message: str, style: str = SUCCESS) -> None:
        """
        Обновляет сообщение в строке состояния.

        Args:
            message: Текст сообщения
            style: Стиль сообщения (SUCCESS, DANGER, INFO)
        """
        self.status_var.set(message)

        # Автоматически очищаем сообщение об ошибке через 5 секунд
        if style == DANGER:
            self.after(5000, lambda: self._update_status("Готов к работе", SUCCESS))