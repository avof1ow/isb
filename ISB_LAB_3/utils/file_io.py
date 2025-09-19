from pathlib import Path
from core.exceptions import CryptoError
from typing import Union


def read_file(path: Union[str, Path]) -> bytes:
    """
    Безопасно читает содержимое файла в бинарном режиме.
    
    Args:
        path: Путь к файлу (строка или объект Path).
    
    Return:
        bytes: Содержимое файла в виде байтов.
    
    Raises:
        CryptoError: Если файл не существует, не является файлом или возникла ошибка чтения.
    """
    try:
        path = Path(path)
        if not path.exists():
            raise CryptoError(f"Файл не найден: {path}")
        if not path.is_file():
            raise CryptoError(f"Указанный путь не является файлом: {path}")
        with open(path, "rb") as file:
            return file.read()
    except IOError as e:
        raise CryptoError(f"Ошибка чтения файла: {str(e)}")


def write_file(path: Union[str, Path], data: bytes) -> bool:
    """
    Безопасно записывает данные в файл в бинарном режиме.
    
    Args:
        path: Путь к файлу (строка или объект Path).
        data: Данные для записи (в байтах).
    
    Return:
        bool: `True`, если запись прошла успешно.
    
    Raises:
        CryptoError: Если возникла ошибка записи.
    """
    try:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as file:
            file.write(data)
        return True
    except IOError as e:
        raise CryptoError(f"Ошибка записи в файл: {str(e)}")