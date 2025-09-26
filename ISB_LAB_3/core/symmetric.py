import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from core.exceptions import KeyGenerationError, EncryptionError, DecryptionError


def generate_symmetric_key(key_size: int = 32) -> bytes:
    """Генерирует симметричный ключ для AES.

    Args:
        key_size: Размер ключа в байтах (по умолчанию 32 = 256 бит)

    Returns:
        bytes: Сгенерированный ключ

    Raises:
        KeyGenerationError: Если генерация не удалась
    """
    try:
        return os.urandom(key_size)
    except Exception as e:
        raise KeyGenerationError(f"Ошибка генерации симметричного ключа: {str(e)}")


def encrypt_data(data: bytes, symmetric_key: bytes) -> bytes:
    """Шифрует данные с помощью AES-CBC.

    Args:
        data: Данные для шифрования
        symmetric_key: Симметричный ключ

    Returns:
        bytes: Зашифрованные данные (IV + ciphertext)

    Raises:
        EncryptionError: Если шифрование не удалось
    """
    try:
        iv = os.urandom(16)
        padder = sym_padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return iv + ciphertext
    except Exception as e:
        raise EncryptionError(f"Ошибка шифрования данных: {str(e)}")


def decrypt_data(ciphertext: bytes, symmetric_key: bytes) -> bytes:
    """Дешифрует данные с помощью AES-CBC.

    Args:
        ciphertext: Зашифрованные данные (IV + ciphertext)
        symmetric_key: Симметричный ключ

    Returns:
        bytes: Расшифрованные данные

    Raises:
        DecryptionError: Если дешифрование не удалось
    """
    try:
        iv = ciphertext[:16]
        data = ciphertext[16:]

        cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(data) + decryptor.finalize()

        unpadder = sym_padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return plaintext
    except Exception as e:
        raise DecryptionError(f"Ошибка дешифрования данных: {str(e)}")