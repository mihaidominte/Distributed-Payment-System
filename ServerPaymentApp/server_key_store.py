import base64
import os
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

KEYS_DIR = "keys"
PRIVATE_KEY_CERTIFICATE_FILE = f"{KEYS_DIR}/server_private_key_certificate.pem"
PUBLIC_KEY_CERTIFICATE_FILE = f"{KEYS_DIR}/server_public_key_certificate.pem"
PRIVATE_KEY_SIGN_FILE = f"{KEYS_DIR}/server_private_key_sign.pem"
PUBLIC_KEY_SIGN_FILE = f"{KEYS_DIR}/server_public_key_sign.pem"

class ServerKeyStore:
    _PRIVATE_KEY_FILE = None
    _PUBLIC_KEY_FILE = None

    def __init__(self):
        self._private_key = None
        self._public_key = None
        self._load_or_generate()

    def _load_or_generate(self) -> None:
        os.makedirs(KEYS_DIR, exist_ok=True)

        if os.path.exists(self._PRIVATE_KEY_FILE):
            self._load_keys()
        else:
            self._generate_and_save_keys()

    def _generate_and_save_keys(self) -> None:
        self._private_key = Ed25519PrivateKey.generate()
        self._public_key = self._private_key.public_key()

        with open(self._PRIVATE_KEY_FILE, "wb") as f:
            f.write(self._private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        with open(self._PUBLIC_KEY_FILE, "wb") as f:
            f.write(self._public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    def _load_keys(self) -> None:
        with open(self._PRIVATE_KEY_FILE, "rb") as f:
            self._private_key = serialization.load_pem_private_key(
                f.read(),
                password=None
            )

        with open(self._PUBLIC_KEY_FILE, "rb") as f:
            self._public_key = serialization.load_pem_public_key(
                f.read()
            )

    def sign(self, message: str) -> str:
        if self._private_key is None:
            raise Exception("Private key not loaded")

        message = base64.b64decode(message)
        signature = self._private_key.sign(message)
        signature = base64.b64encode(signature).decode()
        return signature

    def verify(self, message: bytes, signature: bytes) -> bool:
        try:
            self._public_key.verify(signature, message)
            return True
        except InvalidSignature:
            return False

    def public_key(self):
        return self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

class ServerKeyCertificate(ServerKeyStore):
    _PRIVATE_KEY_FILE = PRIVATE_KEY_CERTIFICATE_FILE
    _PUBLIC_KEY_FILE = PUBLIC_KEY_CERTIFICATE_FILE

class ServerKeySigning(ServerKeyStore):
    _PRIVATE_KEY_FILE = PRIVATE_KEY_SIGN_FILE
    _PUBLIC_KEY_FILE = PUBLIC_KEY_SIGN_FILE