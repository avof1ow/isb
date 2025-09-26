from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from core.exceptions import KeyGenerationError, EncryptionError, DecryptionError


def generate_rsa_key_pair() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Генерирует пару RSA-ключей.

    Returns:
        tuple: Приватный и публичный ключи

    Raises:
        KeyGenerationError: Если генерация не удалась
    """
    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        return private_key, public_key
    except Exception as e:
        raise KeyGenerationError(f"Ошибка генерации RSA-ключей: {str(e)}")


def encrypt_with_rsa(public_key: rsa.RSAPublicKey, data: bytes) -> bytes:
    """Шифрует данные с помощью RSA-OAEP.

    Args:
        public_key: Публичный RSA-ключ
        data: Данные для шифрования

    Returns:
        bytes: Зашифрованные данные

    Raises:
        EncryptionError: Если шифрование не удалось
    """
    try:
        return public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
    except Exception as e:
        raise EncryptionError(f"Ошибка шифрования с RSA: {str(e)}")


def decrypt_with_rsa(private_key: rsa.RSAPrivateKey, encrypted_data: bytes) -> bytes:
    """Дешифрует данные с помощью RSA-OAEP.

    Args:
        private_key: Приватный RSA-ключ
        encrypted_data: Зашифрованные данные

    Returns:
        bytes: Расшифрованные данные

    Raises:
        DecryptionError: Если дешифрование не удалось
    """
    try:
        return private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
    except Exception as e:
        raise DecryptionError(f"Ошибка дешифрования с RSA: {str(e)}")