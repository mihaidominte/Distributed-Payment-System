import uuid
import hashlib
from typing import List, Dict
from database import DatabaseServer
from server_key_store import ServerKeySigning


class TokensManager:
    def __init__(self):
        self.server_key_signing = ServerKeySigning()

    @staticmethod
    def _assign_value() -> int:
        """Atribuie valori tokenilor
        Cand va fi implementata va atribui valori astfel incat
        utilizatorul sa primeasca o catitate echilibrata de tokeni cu valori mici si mari"""

        return 1

    def generate_tokens(self, amount: int, user_id: str) -> List[Dict]:
        tokens = []
        db = DatabaseServer()

        for _ in range(amount):
            token = {"id": str(uuid.uuid4()),
                     "user_id": user_id,
                     "value": self._assign_value()}
            token_hash = hashlib.sha256(str(token.values()).encode()).hexdigest()
            token["hash"] = token_hash
            token_signature = self.server_key_signing.sign(token_hash)
            token["signature"] = token_signature
            db.insert("tokens", token)
            tokens.append(token)

        return tokens

