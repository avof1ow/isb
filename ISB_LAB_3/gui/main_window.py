import tkinter as tk
from tkinter import messagebox, Canvas
import ttkbootstrap as ttk
from ttkbootstrap.constants import DARK, SUCCESS, DANGER, INVERSE, PRIMARY
from gui.widgets import PathSelector
from core import hybrid
from utils.file_io import read_file, write_file
from utils.config_manager import ConfigManager
from typing import Optional
import time
import os 

class MainWindow(ttk.Window):
    """Главное окно приложения."""

    def __init__(self, config_manager: ConfigManager) -> None:
        """Инициализация главного окна приложения.

        Args:
            config_manager (ConfigManager): Менеджер конфигурации.
        
        Return:
            None
        """
        self.config = config_manager
        super().__init__(themename=self.config.get("theme", "darkly"))
        self._setup_window()
        self._create_welcome_screen()
        self.after(100, self._animate_welcome_sequence)

    def _setup_window(self) -> None:
        """Настраивает свойства окна и стили."""
        self.title("Hybrid Crypto System")
        self.geometry("900x650")
        self.minsize(800, 550)

        style = ttk.Style()
        style.configure(".", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 11, "bold"))
        style.configure("TLabel", font=("Segoe UI", 11))
        style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=[15, 5])
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("success.TButton", foreground="white")
        style.configure("info.TLabel", foreground="#2ecc71")

    def _create_welcome_screen(self) -> None:
        """Создает экран приветствия."""
        self.welcome_frame = ttk.Frame(self, bootstyle=DARK)
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)

        # Градиентный фон
        self.canvas = Canvas(self.welcome_frame, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self._create_gradient()

        container = ttk.Frame(self.welcome_frame, bootstyle=DARK)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

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

        self.progress = ttk.Progressbar(
            container,
            mode="determinate",
            maximum=100,
            bootstyle=SUCCESS,
        )
        self.progress.pack(pady=20, fill=tk.X, padx=50)

    def _create_gradient(self) -> None:
        """Рисует градиентный фон на холсте."""
        width = 900
        height = 650
        self.canvas.delete("all")
        for i in range(height):
            r = int(20 + (i / height) * 30)
            g = int(20 + (i / height) * 50)
            b = int(50 + (i / height) * 70)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, width, i, fill=color)

    def _animate_welcome_sequence(self) -> None:
        """Анимирует экран приветствия. """
        for i in range(0, 100, 2):
            self.progress["value"] = i
            self.update()
            time.sleep(0.03)

        for alpha in range(100, -1, -2):
            self.attributes("-alpha", alpha / 100)  # Применить к окну, а не к фрейму
            self.update()
            time.sleep(0.02)

        self.attributes("-alpha", 1.0)  # Сбросить непрозрачность окна
        self.welcome_frame.destroy()
        self._create_main_interface()

    def _create_main_interface(self) -> None:
        """Создаёт интерфейс главного приложения."""
        self._create_widgets()
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=15, pady=15)

    def _create_widgets(self) -> None:
        """Создает виджеты блокнота и статусной строки."""
        self.notebook = ttk.Notebook(self, bootstyle=DARK)
        self._setup_keygen_tab()
        self._setup_encryption_tab()
        self._setup_decryption_tab()

        self.notebook.add(self.key_frame, text="🔑 Генерация ключей")
        self.notebook.add(self.enc_frame, text="🔒 Шифрование")
        self.notebook.add(self.dec_frame, text="🔓 Дешифрование")

        self.status_var = tk.StringVar(value="")
        status_bar = ttk.Frame(self, bootstyle=DARK)
        status_bar.pack(fill=tk.X, padx=5, pady=(0, 5))
        ttk.Label(
            status_bar,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bootstyle=(SUCCESS, INVERSE),
        ).pack(fill=tk.X, expand=True, ipady=3)

    def _setup_keygen_tab(self) -> None:
        """Настройка вкладки генерации ключей."""
        self.key_frame = ttk.Frame(self.notebook, padding=15, bootstyle=DARK)
        frame = ttk.Labelframe(
            self.key_frame,
            text="Настройки генерации ключей",
            padding=(15, 10),
        )
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

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

        for widget in [self.priv_key_sel, self.pub_key_sel, self.enc_key_sel]:
            widget.pack(fill=tk.X, padx=5, pady=8)

        btn_frame = ttk.Frame(frame, bootstyle=DARK)
        btn_frame.pack(fill=tk.X, pady=(15, 5))
        ttk.Button(
            btn_frame,
            text="Сгенерировать ключи",
            command=self._generate_keys,
            bootstyle=SUCCESS,
            width=20,
        ).pack(side=tk.LEFT, padx=5)

        info_frame = ttk.Frame(frame, bootstyle=DARK)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(
            info_frame,
            text="Предупреждение: Приватный ключ должен быть надёжно сохранён!",
            bootstyle=(SUCCESS, INVERSE),
            anchor=tk.CENTER,
            padding=5,
        ).pack(fill=tk.X)

    def _setup_encryption_tab(self) -> None:
        """Настройка вкладки шифрования."""
        self.enc_frame = ttk.Frame(self.notebook, padding=15, bootstyle=DARK)
        frame = ttk.Labelframe(
            self.enc_frame,
            text="Настройки шифрования",
            padding=(15, 10),
        )
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.input_enc_sel = PathSelector(frame, "Файл для шифрования:")
        self.pub_key_enc_sel = PathSelector(
            frame, "Публичный ключ:", [("PEM files", "*.pem")]
        )
        self.enc_key_enc_sel = PathSelector(
            frame, "Зашифрованный ключ:", [("BIN files", "*.bin")]
        )
        self.output_enc_sel = PathSelector(
            frame,
            "Выходной файл:",
            is_save=True,
            initialfile=self.config.get("default_paths.encrypted_file", "encrypted.bin"),
        )

        for widget in [
            self.input_enc_sel,
            self.pub_key_enc_sel,  
            self.enc_key_enc_sel,
            self.output_enc_sel,
        ]:
            widget.pack(fill=tk.X, padx=5, pady=8)

        btn_frame = ttk.Frame(frame, bootstyle=DARK)
        btn_frame.pack(fill=tk.X, pady=(15, 5))
        ttk.Button(
            btn_frame,
            text="Зашифровать файл",
            command=self._encrypt,
            bootstyle=SUCCESS,
            width=20,
        ).pack(side=tk.LEFT, padx=5)

    def _setup_decryption_tab(self) -> None:
        """Настройка вкладки дешифрования."""
        self.dec_frame = ttk.Frame(self.notebook, padding=15, bootstyle=DARK)
        frame = ttk.Labelframe(
            self.dec_frame,
            text="Настройки дешифрования",
            padding=(15, 10),
        )
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.input_dec_sel = PathSelector(frame, "Файл для дешифрования:")
        self.priv_key_dec_sel = PathSelector(
            frame, "Приватный ключ:", [("PEM files", "*.pem")]
        )
        self.enc_key_dec_sel = PathSelector(
            frame, "Зашифрованный ключ:", [("BIN files", "*.bin")]
        )
        self.output_dec_sel = PathSelector(
            frame,
            "Выходной файл:",
            is_save=True,
            initialfile=self.config.get("default_paths.decrypted_file", "decrypted.txt"),
        )

        for widget in [
            self.input_dec_sel,
            self.priv_key_dec_sel,
            self.enc_key_dec_sel,
            self.output_dec_sel,
        ]:
            widget.pack(fill=tk.X, padx=5, pady=8)

        btn_frame = ttk.Frame(frame, bootstyle=DARK)
        btn_frame.pack(fill=tk.X, pady=(15, 5))
        ttk.Button(
            btn_frame,
            text="Расшифровать файл",
            command=self._decrypt,
            bootstyle=SUCCESS,
            width=20,
        ).pack(side=tk.LEFT, padx=5)

    def _generate_keys(self) -> None:
        """Генерирует и сохраняет RSA ключи."""
        try:
            keys = hybrid.generate_rsa_keys()
            write_file(self.priv_key_sel.path or self.config.get("default_paths.private_key"), keys["private_key"])
            write_file(self.pub_key_sel.path or self.config.get("default_paths.public_key"), keys["public_key"])
            self._update_status("Ключи успешно сгенерированы!", SUCCESS)
            messagebox.showinfo("Успех", "Ключи успешно сгенерированы!", parent=self)
        except Exception as e:
            self._update_status(f"Ошибка: {str(e)}", DANGER)
            messagebox.showerror("Ошибка", str(e), parent=self)

    def _encrypt(self) -> None:
        """Шифрует файл."""
        try:
            public_key_pem = read_file(self.pub_key_enc_sel.path)
            plaintext = read_file(self.input_enc_sel.path)
            result = hybrid.hybrid_encrypt(plaintext, public_key_pem)
            write_file(self.enc_key_enc_sel.path, result["encrypted_symmetric"])
            write_file(self.output_enc_sel.path, result["ciphertext"])
            self._update_status("Шифрование выполнено успешно!", SUCCESS)
            messagebox.showinfo("Успех", "Шифрование выполнено успешно!", parent=self)
        except Exception as e:
            self._update_status(f"Ошибка: {str(e)}", DANGER)
            messagebox.showerror("Ошибка", str(e), parent=self)

    def _decrypt(self) -> None:
        """Дешифрует файл."""
        try:
            private_key_pem = read_file(self.priv_key_dec_sel.path)
            encrypted_symmetric = read_file(self.enc_key_dec_sel.path)
            ciphertext = read_file(self.input_dec_sel.path)
            plaintext = hybrid.hybrid_decrypt(ciphertext, encrypted_symmetric, private_key_pem)
            write_file(self.output_dec_sel.path, plaintext)
            self._update_status("Дешифрование выполнено успешно!", SUCCESS)
            messagebox.showinfo("Успех", "Дешифрование выполнено успешно!", parent=self)
        except Exception as e:
            self._update_status(f"Ошибка: {str(e)}", DANGER)
            messagebox.showerror("Ошибка", str(e), parent=self)

    def _update_status(self, message: str, style: str = SUCCESS) -> None:
        """Обновляет строку состояния с сообщением и стилем.

        Args:
            message (str): Сообщение для отображения в статусной строке.
            style (str, optional): Стиль сообщения. По умолчанию - SUCCESS.

        Return:
            None
        """
        self.status_var.set(message)
        for child in self.winfo_children():
            if isinstance(child, ttk.Frame) and child.winfo_children():
                status_label = child.winfo_children()[0]
                status_label.configure(bootstyle=(style, INVERSE))

        if style != SUCCESS:
            self.after(5000, lambda: self._update_status("", SUCCESS))