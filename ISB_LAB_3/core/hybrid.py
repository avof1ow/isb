from typing import Dict
from core import asymmetric, symmetric, serialization
from core.exceptions import CryptoError


def generate_rsa_keys() -> Dict[str, bytes]:
    """Генерирует пару RSA-ключей.

    Returns:
        Dict: Словарь с приватным и публичным ключами в PEM-формате

    Raises:
        CryptoError: Если генерация не удалась
    """
    try:
        private_key, public_key = asymmetric.generate_rsa_key_pair()
        private_pem = serialization.serialize_private_key(private_key)
        public_pem = serialization.serialize_public_key(public_key)
        return {"private_key": private_pem, "public_key": public_pem}
    except Exception as e:
        raise CryptoError(f"Ошибка генерации RSA-ключей: {str(e)}")


def hybrid_encrypt(plaintext: bytes, public_key_pem: bytes) -> Dict[str, bytes]:
    """Шифрует данные гибридным методом (RSA + AES).

    Args:
        plaintext: Данные для шифрования
        public_key_pem: Публичный ключ в PEM-формате

    Returns:
        Dict: Словарь с зашифрованным ключом и данными

    Raises:
        CryptoError: Если шифрование не удалось
    """
    try:
        public_key = serialization.deserialize_public_key(public_key_pem)
        symmetric_key = symmetric.generate_symmetric_key()
        encrypted_symmetric = asymmetric.encrypt_with_rsa(public_key, symmetric_key)
        ciphertext = symmetric.encrypt_data(plaintext, symmetric_key)
        return {"encrypted_symmetric": encrypted_symmetric, "ciphertext": ciphertext}
    except Exception as e:
        raise CryptoError(f"Ошибка шифрования: {str(e)}")


def hybrid_decrypt(ciphertext: bytes, encrypted_symmetric: bytes, private_key_pem: bytes) -> bytes:
    """Дешифрует данные гибридным методом.

    Args:
        ciphertext: Зашифрованные данные
        encrypted_symmetric: Зашифрованный симметричный ключ
        private_key_pem: Приватный ключ в PEM-формате

    Returns:
        bytes: Расшифрованные данные

    Raises:
        CryptoError: Если дешифрование не удалось
    """
    try:
        private_key = serialization.deserialize_private_key(private_key_pem)
        symmetric_key = asymmetric.decrypt_with_rsa(private_key, encrypted_symmetric)
        plaintext = symmetric.decrypt_data(ciphertext, symmetric_key)
        return plaintext
    except Exception as e:
        raise CryptoError(f"Ошибка дешифрования: {str(e)}")
