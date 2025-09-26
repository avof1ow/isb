import logging
from pathlib import Path
from typing import Union

from core.exceptions import FileOperationError

logger = logging.getLogger(__name__)


def read_file(path: Union[str, Path]) -> bytes:
    """
    Безопасно читает содержимое файла в бинарном режиме.

    Args:
        path: Путь к файлу (строка или объект Path)

    Returns:
        bytes: Содержимое файла в виде байтов

    Raises:
        FileOperationError: Если файл не существует или возникла ошибка чтения
    """
    try:
        path = Path(path)

        if not path.exists():
            raise FileOperationError(f"Файл не найден: {path}")

        if not path.is_file():
            raise FileOperationError(f"Указанный путь не является файлом: {path}")

        with open(path, "rb") as file:
            content = file.read()

        logger.debug(f"Файл прочитан успешно: {path} ({len(content)} байт)")
        return content

    except FileOperationError:
        raise  # Пробрасываем уже известные ошибки
    except IOError as e:
        error_msg = f"Ошибка чтения файла {path}: {str(e)}"
        logger.error(error_msg)
        raise FileOperationError(error_msg) from e


def write_file(path: Union[str, Path], data: bytes) -> bool:
    """
    Безопасно записывает данные в файл в бинарном режиме.

    Args:
        path: Путь к файлу (строка или объект Path)
        data: Данные для записи (в байтах)

    Returns:
        bool: True если запись прошла успешно

    Raises:
        FileOperationError: Если возникла ошибка записи
    """
    try:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "wb") as file:
            file.write(data)

        logger.debug(f"Файл записан успешно: {path} ({len(data)} байт)")
        return True

    except IOError as e:
        error_msg = f"Ошибка записи в файл {path}: {str(e)}"
        logger.error(error_msg)
        raise FileOperationError(error_msg) from e