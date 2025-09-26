from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from core.exceptions import FileOperationError


def serialize_private_key(private_key: rsa.RSAPrivateKey) -> bytes:
    """Сериализует приватный RSA-ключ в PEM-формат.

    Args:
        private_key: Приватный RSA-ключ

    Returns:
        bytes: PEM-данные приватного ключа
    """
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def deserialize_private_key(private_key_pem: bytes) -> rsa.RSAPrivateKey:
    """Десериализует приватный RSA-ключ из PEM-данных.

    Args:
        private_key_pem: PEM-данные приватного ключа

    Returns:
        rsa.RSAPrivateKey: Приватный ключ

    Raises:
        FileOperationError: Если десериализация не удалась
    """
    try:
        return serialization.load_pem_private_key(private_key_pem, password=None)
    except Exception as e:
        raise FileOperationError(f"Ошибка загрузки приватного ключа: {str(e)}")


def serialize_public_key(public_key: rsa.RSAPublicKey) -> bytes:
    """Сериализует публичный RSA-ключ в PEM-формат.

    Args:
        public_key: Публичный RSA-ключ

    Returns:
        bytes: PEM-данные публичного ключа
    """
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def deserialize_public_key(public_key_pem: bytes) -> rsa.RSAPublicKey:
    """Десериализует публичный RSA-ключ из PEM-данных.

    Args:
        public_key_pem: PEM-данные публичного ключа

    Returns:
        rsa.RSAPublicKey: Публичный ключ

    Raises:
        FileOperationError: Если десериализация не удалась
    """
    try:
        return serialization.load_pem_public_key(public_key_pem)
    except Exception as e:
        raise FileOperationError(f"Ошибка загрузки публичного ключа: {str(e)}")