from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from core.exceptions import CryptoError

def generate_rsa_key_pair() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Генерирует пару RSA-ключей.

    Return:
        tuple: Приватный и публичный ключи (rsa.RSAPrivateKey, rsa.RSAPublicKey).

    Raises:
        CryptoError: Если генерация не удалась.
    """
    try:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        return private_key, public_key
    except Exception as e:
        raise CryptoError(f"Ошибка генерации RSA-ключей: {str(e)}")

def encrypt_with_rsa(public_key: rsa.RSAPublicKey, data: bytes) -> bytes:
    """Шифрует данные с помощью RSA.

    Args:
        public_key: Публичный RSA-ключ.
        data: Данные для шифрования (например, симметричный ключ).

    Return:
        bytes: Зашифрованные данные.

    Raises:
        CryptoError: Если шифрование не удалось.
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
        raise CryptoError(f"Ошибка шифрования с RSA: {str(e)}")

def decrypt_with_rsa(private_key: rsa.RSAPrivateKey, encrypted_data: bytes) -> bytes:
    """Дешифрует данные с помощью RSA.

    Args:
        private_key: Приватный RSA-ключ.
        encrypted_data: Зашифрованные данные.

    Return:
        bytes: Расшифрованные данные.

    Raises:
        CryptoError: Если дешифрование не удалось.
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
        raise CryptoError(f"Ошибка дешифрования с RSA: {str(e)}")
