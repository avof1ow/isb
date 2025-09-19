from tkinter import ttk
from PIL import Image, ImageTk
from typing import Optional

def configure_styles(root: ttk.Widget) -> None:
    """Настроить стили приложения и загрузить иконки.

    Args:
        root (ttk.Widget): Корневой виджет приложения.
    
    Return:
        None
    """
    style = ttk.Style(root)
    style.theme_use("clam")

    # Конфигурация цветов
    colors = {
        "background": "#f0f0f0",
        "accent": "#4a6ea9",
        "text": "#333333",
        "tab_background": "#d9d9d9",
        "field_background": "white",
    }

    # Базовая конфигурация стиля
    style.configure(
        ".",
        background=colors["background"],
        foreground=colors["text"],
        font=("Segoe UI", 10),
    )
    style.configure("TFrame", background=colors["background"])
    style.configure("TLabel", background=colors["background"])
    style.configure(
        "TButton",
        background=colors["accent"],
        foreground="white",
        padding=6,
    )
    style.configure("TNotebook", background=colors["background"])
    style.configure(
        "TNotebook.Tab",
        padding=[10, 5],
        background=colors["tab_background"],
    )
    style.map("TNotebook.Tab", background=[("selected", colors["accent"])]
)
    style.configure("TEntry", fieldbackground=colors["field_background"])

    # Загрузка иконок
    root.folder_icon = load_icon("assets/folder.png", size=(16, 16))

def load_icon(path: str, size: tuple[int, int]) -> Optional[ImageTk.PhotoImage]:
    """Загрузить и изменить размер иконки.

    Args:
        path (str): Путь к файлу иконки.
        size (tuple[int, int]): Новый размер иконки.
    
    Return:
        Optional[ImageTk.PhotoImage]: Изменённая иконка или None в случае ошибки.
    """
    try:
        image = Image.open(path).resize(size)
        return ImageTk.PhotoImage(image)
    except Exception:
        return None