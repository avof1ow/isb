import logging
from pathlib import Path
from tkinter import ttk
from typing import Optional

from PIL import Image, ImageTk
from utils.config_manager import ConfigManager

# Настройка логирования
logger = logging.getLogger(__name__)


def configure_styles(root: ttk.Widget, config: ConfigManager) -> None:
    """
    Настраивает стили приложения на основе конфигурации.

    Args:
        root: Корневой виджет приложения
        config: Менеджер конфигурации с настройками цветов и путей
    """
    style = ttk.Style(root)
    style.theme_use("clam")

    # Получаем цвета из конфигурации
    colors = config.get("colors", {})

    # Настраиваем стили виджетов
    _configure_widget_styles(style, colors)

    # Загружаем иконки
    _load_icons(root, config)


def _configure_widget_styles(style: ttk.Style, colors: dict) -> None:
    """
    Настраивает стили для различных виджетов.

    Args:
        style: Объект стилей ttk
        colors: Словарь с цветовыми настройками
    """
    # Базовая конфигурация
    style.configure(
        ".",
        background=colors.get("background", "#f0f0f0"),
        foreground=colors.get("text", "#333333"),
        font=("Segoe UI", 10),
    )

    # Стили для конкретных виджетов
    style.configure("TFrame", background=colors.get("background", "#f0f0f0"))
    style.configure("TLabel", background=colors.get("background", "#f0f0f0"))
    style.configure(
        "TButton",
        background=colors.get("accent", "#4a6ea9"),
        foreground="white",
        padding=6,
    )
    style.configure("TNotebook", background=colors.get("background", "#f0f0f0"))
    style.configure(
        "TNotebook.Tab",
        padding=[10, 5],
        background=colors.get("tab_background", "#d9d9d9"),
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", colors.get("accent", "#4a6ea9"))]
    )
    style.configure(
        "TEntry",
        fieldbackground=colors.get("field_background", "white")
    )


def _load_icons(root: ttk.Widget, config: ConfigManager) -> None:
    """
    Загружает иконки для приложения.

    Args:
        root: Корневой виджет для хранения иконок
        config: Менеджер конфигурации с путями к иконкам
    """
    icon_path = config.get("icons.folder", "")
    if icon_path:
        root.folder_icon = _load_icon_safe(icon_path, (16, 16))
    else:
        logger.warning("Путь к иконке папки не указан в конфигурации")


def _load_icon_safe(path: str, size: tuple[int, int]) -> Optional[ImageTk.PhotoImage]:
    """
    Безопасно загружает иконку с обработкой ошибок.

    Args:
        path: Путь к файлу иконки
        size: Размер иконки (ширина, высота)

    Returns:
        ImageTk.PhotoImage или None в случае ошибки
    """
    try:
        # Проверяем существование файла
        if not Path(path).exists():
            logger.error(f"Файл иконки не найден: {path}")
            return None

        image = Image.open(path).resize(size)
        return ImageTk.PhotoImage(image)

    except Exception as e:
        logger.error(f"Ошибка загрузки иконки {path}: {e}")
        return None
