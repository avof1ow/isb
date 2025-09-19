import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY, OUTLINE
from pathlib import Path
from typing import Tuple, Optional

class PathSelector(ttk.Frame):
    """Виджет для выбора файлов с полем ввода и кнопкой обзора."""

    def __init__(
        self,
        master: tk.Misc,
        title: str,
        filetypes: Tuple[Tuple[str, str], ...] = (),
        is_save: bool = False,
        initialfile: str = "",
    ) -> None:
        """
        Инициализация PathSelector.

        Args:
            master (tk.Misc): Родительский виджет.
            title (str): Текст подписи.
            filetypes (Tuple[Tuple[str, str], ...], optional): Фильтры файлов (пример: [("Текстовые файлы", "*.txt")]). По умолчанию - пустой кортеж.
            is_save (bool, optional): Режим сохранения (True) или открытия (False). По умолчанию - False.
            initialfile (str, optional): Имя файла по умолчанию. По умолчанию - пустая строка.

        Return:
            None
        """
        super().__init__(master)
        self.title = title
        self.filetypes = filetypes
        self.is_save = is_save
        self.initialfile = initialfile
        self.path_var = tk.StringVar()
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Создает элементы интерфейса виджета."""
        ttk.Label(self, text=self.title, bootstyle=PRIMARY).pack(side=tk.LEFT, padx=5)

        entry = ttk.Entry(self, textvariable=self.path_var, width=40)
        entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        btn_text = "Сохранить" if self.is_save else "Обзор"
        ttk.Button(
            self,
            text=btn_text,
            command=self._browse,
            bootstyle=(OUTLINE, PRIMARY),
            width=8,
        ).pack(side=tk.LEFT)

    def _browse(self) -> None:
        """Открывает диалоговое окно для выбора файла."""
        initial_dir = Path.home()
        if self.path_var.get():
            initial_dir = Path(self.path_var.get()).parent

        path: Optional[str] = None
        if self.filetypes:
            if self.is_save:
                path = filedialog.asksaveasfilename(
                    initialdir=initial_dir,
                    filetypes=self.filetypes,
                    initialfile=self.initialfile,
                )
            else:
                path = filedialog.askopenfilename(
                    initialdir=initial_dir,
                    filetypes=self.filetypes,
                )
        else:
            if self.is_save:
                path = filedialog.asksaveasfilename(
                    initialdir=initial_dir,
                    initialfile=self.initialfile,
                )
            else:
                path = filedialog.askopenfilename(initialdir=initial_dir)

        if path:
            self.path_var.set(path)

    @property
    def path(self) -> str:
        """Возвращает выбранный путь.

        Return:
            str: Путь к файлу
        """
        return self.path_var.get()