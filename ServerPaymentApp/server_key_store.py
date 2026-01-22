from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

KEYS_DIR = "keys"
PRIVATE_KEY_FILE = f"{KEYS_DIR}/server_private.pem"
PUBLIC_KEY_FILE = f"{KEYS_DIR}/server_public.pem"

class ServerKeyStore:
    _private_key = None
    _public_key = None
    _server_id = "PAYMENT_SERVER_V1"

    @classmethod
    def load_or_generate(cls):
        os.makedirs(KEYS_DIR, exist_ok=True)

        if os.path.exists(PRIVATE_KEY_FILE):
            cls._load_keys()
        else:
            cls._generate_and_save_keys()

    @classmethod
    def _generate_and_save_keys(cls):
        cls._private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        cls._public_key = cls._private_key.public_key()

        with open(PRIVATE_KEY_FILE, "wb") as f:
            f.write(cls._private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        with open(PUBLIC_KEY_FILE, "wb") as f:
            f.write(cls._public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    @classmethod
    def _load_keys(cls):
        with open(PRIVATE_KEY_FILE, "rb") as f:
            cls._private_key = serialization.load_pem_private_key(
                f.read(),
                password=None
            )

        with open(PUBLIC_KEY_FILE, "rb") as f:
            cls._public_key = serialization.load_pem_public_key(
                f.read()
            )

    @classmethod
    def server_id(cls):
        return cls._server_id

    @classmethod
    def private_key(cls):
        return cls._private_key

    @classmethod
    def public_key(cls):
        return cls._public_key