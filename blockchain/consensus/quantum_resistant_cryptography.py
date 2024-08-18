import hashlib
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

class QuantumResistantCryptography:
    def __init__(self, private_key=None, public_key=None):
        self.private_key = private_key
        self.public_key = public_key
        if not private_key and not public_key:
            self.generate_key_pair()

    def generate_key_pair(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()

    def get_public_key_pem(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def get_private_key_pem(self):
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

    def encrypt(self, data):
        cipher = self.public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return cipher

    def decrypt(self, encrypted_data):
        plaintext = self.private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext

    def derive_key(self, salt, info):
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            info=info,
        )
        key = hkdf.derive(self.private_key.exchange(self.public_key))
        return key

     def __str__(self):
        return f"Quantum Resistant Cryptography (Private Key: {self.private_key}, Public Key: {self.public_key})"

# Example usage:
if __name__ == '__main__':
    crypto = QuantumResistantCryptography()

    # Generate a key pair
    private_key_pem = crypto.get_private_key_pem()
    public_key_pem = crypto.get_public_key_pem()

    # Encrypt some data
    data = b"Hello, World!"
    encrypted_data = crypto.encrypt(data)

    # Decrypt the data
    decrypted_data = crypto.decrypt(encrypted_data)

    # Derive a key
    salt = os.urandom(16)
    info = b"my_info"
    derived_key = crypto.derive_key(salt, info)

    print(f"Private Key PEM: {private_key_pem}")
    print(f"Public Key PEM: {public_key_pem}")
    print(f"Encrypted Data: {encrypted_data}")
    print(f"Decrypted Data: {decrypted_data}")
    print(f"Derived Key: {derived_key}")
