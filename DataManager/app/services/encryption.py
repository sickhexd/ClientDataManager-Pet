from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
import os

# Функция для генерации случайного ключа
def generate_key():
    return os.urandom(32)

# Функция для шифрования данных
def encrypt_data(data, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_data = data + (16 - len(data) % 16) * ' ' 
    encrypted = encryptor.update(padded_data.encode()) + encryptor.finalize()
    return b64encode(iv + encrypted).decode()  

# Функция для расшифровки данных
def decrypt_data(encrypted_data, key):
    encrypted_data = b64decode(encrypted_data)
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted.decode().rstrip()
