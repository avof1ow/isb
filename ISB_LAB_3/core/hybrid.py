from typing import Dict
from core import symmetric, asymmetric, serialization
from core.exceptions import CryptoError

def generate_rsa_keys() -> Dict[str, bytes]:
    """Генерирует пару RSA-ключей (public + private).

    Return:
        str, bytes: {'private_key': приватный PEM-ключ, 'public_key': публичный PEM-данные}.

    Raises:
        CryptoError: если генерация не удалась.
    """
    try:
        private_key, public_key = asymmetric.generate_rsa_key_pair()
        private_pem = serialization.serialize_private_key(private_key)
        public_pem = serialization.serialize_public_key(public_key)
        return {"private_key": private_pem, "public_key": public_pem}
    except Exception as e:
        raise CryptoError(f"Ошибка генерации RSA-ключей: {str(e)}")

def hybrid_encrypt(plaintext: bytes, public_key_pem: bytes) -> Dict[str, bytes]:
    """Шифрует данные.

    Args:
        plaintext: данные для шифрования.
        public_key_pem: публичный PEM-ключ.

    Return:
        str, bytes: {'encrypted_symmetric': зашифрованный ключ, 'ciphertext': зашифрованные данные}.

    Raises:
        CryptoError: Если шифрование не удалось.
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
    """Дешифрует данные.

    Args:
        ciphertext: хашифрованные данные.
        encrypted_symmetric: зашифрованный симметричный ключ.
        private_key_pem: приватный PEM-ключ.

    Return:
        bytes: расшифрованные данные.

    Raises:
        CryptoError: если дешифрование не удалось.
    """
    try:
        private_key = serialization.deserialize_private_key(private_key_pem)
        symmetric_key = asymmetric.decrypt_with_rsa(private_key, encrypted_symmetric)
        plaintext = symmetric.decrypt_data(ciphertext, symmetric_key)
        return plaintext
    except Exception as e:
        raise CryptoError(f"Ошибка дешифрования: {str(e)}")
