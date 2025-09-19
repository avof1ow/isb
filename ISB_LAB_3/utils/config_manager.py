import json
from pathlib import Path
from typing import Any, Optional


class ConfigManager:
    """
    Менеджер конфигурации приложения. Работает с JSON-файлами.
    Позволяет:
    - Загружать и сохранять настройки.
    - Получать/устанавливать значения по вложенным ключам (через точку, например, "ui_settings.theme").
    - Автоматически создавать файл конфигурации с настройками по умолчанию, если он отсутствует.
    """

    def __init__(self, config_path: str = "config/settings.json") -> None:
        """
        Args:
            config_path: Путь к JSON-файлу с настройками. По умолчанию: `config/settings.json`.
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        """Загружает конфигурацию из файла. Если файла нет, создает конфиг с настройками по умолчанию.
        
        Return:
            dict: Словарь с текущими настройками.
        """
        try:
            with open(self.config_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            default_config = {"default_paths": {}, "ui_settings": {}}
            self._save_config(default_config)
            return default_config

    def _save_config(self, config: dict[str, Any]) -> None:
        """Сохраняет конфиг в файл. Создает директорию, если она не существует."""
        self.config_path.parent.mkdir(exist_ok=True)
        with open(self.config_path, "w") as file:
            json.dump(config, file, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        """Получает значение из конфигурации по вложенному ключу (через точку).
        
        Args:
            key: Ключ в формате "раздел.подраздел" (например, "default_paths.private_key").
            default: Значение, возвращаемое если ключ не найден.
        
        Return:
            Any: Найденное значение или `default`.
        """
        keys = key.split(".")
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except KeyError:
            return default

    def set(self, key: str, value: Any) -> None:
        """Устанавливает значение в конфигурации по вложенному ключу.
        
        Args:
            key: Ключ.
            value: Значение для сохранения.
        """
        keys = key.split(".")
        current = self.config
        for k in keys[:-1]:
            current = current.setdefault(k, {})
        current[keys[-1]] = value
        self._save_config(self.config)