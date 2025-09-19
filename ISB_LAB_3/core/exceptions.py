class CryptoError(Exception):
    """Базовое исключение для всех ошибок криптографических операций."""


class KeyGenerationError(CryptoError):
    """Исключение при генерации ключей."""


class EncryptionError(CryptoError):
    """Исключение при шифровании данных."""


class DecryptionError(CryptoError):
    """Исключение при дешифровании данных."""


class FileOperationError(CryptoError):
    """Исключение при операциях с файлами (чтение/запись)."""