import tkinter as tk
from enum import Enum
from pathlib import Path
from tkinter import filedialog
from typing import Optional, Tuple

import ttkbootstrap as ttk
from ttkbootstrap.constants import OUTLINE, PRIMARY


class DialogMode(Enum):
    """Режимы работы диалога выбора файла."""
    OPEN = "open"
    SAVE = "save"


class PathSelector(ttk.Frame):
    """
    Виджет для выбора файлов с полем ввода и кнопкой обзора.

    Позволяет пользователю выбирать файлы через диалоговое окно
    или вводить путь вручную.
    """

    def __init__(
            self,
            master: tk.Misc,
            title: str,
            filetypes: Tuple[Tuple[str, str], ...] = (),
            is_save: bool = False,
            initialfile: str = "",
    ) -> None:
        """
        Инициализирует виджет выбора пути.

        Args:
            master: Родительский виджет
            title: Текст подписи
            filetypes: Фильтры файлов (пример: [("Текстовые файлы", "*.txt")])
            is_save: Режим сохранения (True) или открытия (False)
            initialfile: Имя файла по умолчанию
        """
        super().__init__(master)
        self.title = title
        self.filetypes = filetypes
        self.mode = DialogMode.SAVE if is_save else DialogMode.OPEN
        self.initialfile = initialfile
        self.path_var = tk.StringVar()
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Создает и размещает элементы интерфейса виджета."""
        # Метка с названием поля
        ttk.Label(self, text=self.title, bootstyle=PRIMARY).pack(side=tk.LEFT, padx=5)

        # Поле для ввода пути
        entry = ttk.Entry(self, textvariable=self.path_var, width=40)
        entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # Кнопка выбора файла
        btn_text = "Сохранить" if self.mode == DialogMode.SAVE else "Обзор"
        ttk.Button(
            self,
            text=btn_text,
            command=self._open_file_dialog,
            bootstyle=(OUTLINE, PRIMARY),
            width=8,
        ).pack(side=tk.LEFT)

    def _get_initial_directory(self) -> Path:
        """
        Определяет начальную директорию для диалога.

        Returns:
            Path: Путь к начальной директории
        """
        if current_path := self.path_var.get():
            return Path(current_path).parent
        return Path.home()

    def _open_file_dialog(self) -> None:
        """Открывает диалоговое окно для выбора файла."""
        initial_dir = self._get_initial_directory()

        # Подготавливаем параметры для диалога
        dialog_params = {
            "initialdir": initial_dir,
            "filetypes": self.filetypes,
        }

        if self.mode == DialogMode.SAVE:
            dialog_params["initialfile"] = self.initialfile

        # Используем match/case для выбора типа диалога
        match self.mode:
            case DialogMode.SAVE:
                path = filedialog.asksaveasfilename(**dialog_params)
            case DialogMode.OPEN:
                path = filedialog.askopenfilename(**dialog_params)
            case _:
                path = None

        if path:
            self.path_var.set(path)

    @property
    def path(self) -> str:
        """
        Возвращает выбранный путь.

        Returns:
            str: Путь к выбранному файлу
        """
        return self.path_var.get()
