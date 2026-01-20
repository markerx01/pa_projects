from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import socket
import ssl
import hashlib
import secrets

SALT = b"fixed_shared_salt"

def Client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(client_socket)
    ssl_sock.connect(('127.0.0.1', 8080))
    return ssl_sock

def derive_key_from_secret(secret: bytes, salt: bytes):
    return hashlib.pbkdf2_hmac(
        'sha256',
        secret,
        salt,
        100_000,
        32   # 32 bytes = AES-256
    )

def encrypt_data(data: bytes, key: bytes):
    aesgcm = AESGCM(key)
    nonce = secrets.token_bytes(12)
    ciphertext = aesgcm.encrypt(nonce, data, associated_data=None)
    return nonce + ciphertext

def main():
    ssl_sock = Client()

    secret = ssl_sock.recv(1024).strip()
    print("Secret received (bytes):", secret)

    key = derive_key_from_secret(secret, SALT)
    print("Derived key (bytes):", key)
    print("Key length:", len(key))

    filepath = ssl_sock.recv(1024).decode()
    with open(filepath, "rb") as file:
        data = file.read()
    encrypted_data = encrypt_data(data, key)
    output_path = filepath + ".enc"
    with open(output_path, "wb") as f:
        f.write(encrypted_data)


if __name__ == '__main__':
    main()
