import json
from pathlib import Path
from typing import Any, Optional


class ConfigManager:
    """
    Менеджер конфигурации приложения.

    Обеспечивает работу с JSON-файлами настроек, поддерживает
    вложенные ключи через точечную нотацию.
    """

    def __init__(self, config_path: str = "config/settings.json") -> None:
        """
        Инициализирует менеджер конфигурации.

        Args:
            config_path: Путь к JSON-файлу с настройками
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        """
        Загружает конфигурацию из файла.

        Returns:
            Словарь с настройками

        Raises:
            FileNotFoundError: Если файл не существует
            JSONDecodeError: Если файл содержит некорректный JSON
        """
        try:
            with open(self.config_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # Создаем конфиг по умолчанию при ошибке загрузки
            default_config = self._get_default_config()
            self._save_config(default_config)
            return default_config

    def _get_default_config(self) -> dict[str, Any]:
        """
        Возвращает конфигурацию по умолчанию.

        Returns:
            Словарь с настройками по умолчанию
        """
        return {
            "default_paths": {
                "private_key": "private.pem",
                "public_key": "public.pem",
                "encrypted_key": "encrypted_key.bin",
                "encrypted_file": "encrypted.bin",
                "decrypted_file": "decrypted.txt"
            },
            "theme": "darkly",
            "colors": {
                "background": "#f0f0f0",
                "accent": "#4a6ea9",
                "text": "#333333",
                "tab_background": "#d9d9d9",
                "field_background": "white"
            },
            "icons": {
                "folder": "assets/folder.png"
            }
        }

    def _save_config(self, config: dict[str, Any]) -> None:
        """
        Сохраняет конфигурацию в файл.

        Args:
            config: Словарь с настройками для сохранения
        """
        self.config_path.parent.mkdir(exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as file:
            json.dump(config, file, indent=4, ensure_ascii=False)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Получает значение из конфигурации по ключу.

        Args:
            key: Ключ в формате "раздел.подраздел"
            default: Значение по умолчанию при отсутствии ключа

        Returns:
            Найденное значение или default
        """
        keys = key.split(".")
        value = self.config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any) -> None:
        """
        Устанавливает значение в конфигурации.

        Args:
            key: Ключ в формате "раздел.подраздел"
            value: Значение для установки
        """
        keys = key.split(".")
        current = self.config

        for k in keys[:-1]:
            current = current.setdefault(k, {})

        current[keys[-1]] = value
        self._save_config(self.config)
