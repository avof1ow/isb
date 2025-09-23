class CryptoError(Exception):
    """Базовое исключение для всех ошибок криптографических операций."""
    pass


class KeyGenerationError(CryptoError):
    """Исключение при генерации ключей."""
    pass


class EncryptionError(CryptoError):
    """Исключение при шифровании данных."""
    pass


class DecryptionError(CryptoError):
    """Исключение при дешифровании данных."""
    pass


class FileOperationError(CryptoError):
    """Исключение при операциях с файлами (чтение/запись)."""
    pass
