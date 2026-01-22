import time
from database import DatabaseServer
import server_key_store
import utils

class TokensManager:
    def __init__(self, db: DatabaseServer):
        self.db = db
        self.server_key_store = server_key_store.ServerKeyStore()
        self.server_id = self.server_key_store.server_id()
        self.server_private_key = self.server_key_store.private_key()
        self.server_public_key = self.server_key_store.public_key()
        self.calculated_balance = -1

    def generate_genesis_token(self, user_id: str)-> dict:
        date = int(time.time())
        token_hash = utils.calculate_genesis_token_hash(
            self.server_id, user_id, self.calculated_balance, date)

        server_sig = utils.sign_hash(token_hash, self.server_private_key)
        server_token = {
            "id": user_id,
            "sender_id": self.server_id,
            "receiver_id": user_id,
            "amount": self.calculated_balance,
            "date": date,
            "hash": token_hash,
            "signature": None,
            "counter_sig": server_sig,
            "previous_hash": None,
        }
        return server_token

    def validate_user_blockchain(self, blockchain: list[dict]) -> bool:
        if not blockchain:
            utils.print_error("No blockchain")
            return False

        user_id = blockchain[0]["user_id"]
        user_public_key = self.db.get_one("users", "id = ?", (user_id,))["public_key"]
        if not utils.check_owner_chain(user_id, blockchain):
            utils.print_error("Invalid owner")
            return False

        for token in blockchain:
            if not utils.check_token_integrity(token):
                utils.print_error("Token integrity check failed")
                return False

            if token["previous_hash"] is None:
                partner_public_key = self.server_public_key
            elif token["sender_id"] != user_id:
                partner = self.db.get_one("users", "id = ?", (token["sender_id"],))
                if partner is not None:
                    partner_public_key = partner["public_key"]
                else:
                    partner_public_key = None
            else:
                partner = self.db.get_one("users", "id = ?", (token["receiver_id"],))
                if partner is not None:
                    partner_public_key = partner["public_key"]
                else:
                    partner_public_key = None

            if not partner_public_key:
                utils.print_error("Token partner check failed")
                return False
            elif not utils.check_sign(token["hash"], token["signature"], user_public_key):
                utils.print_error("Token signature check failed")
                return False
            elif not utils.check_sign(token["hash"], token["counter_sig"], partner_public_key):
                utils.print_error("Token signature check failed")
                return False

        ordered_blockchain = utils.rebuild_chain(blockchain)
        if ordered_blockchain is False:
            utils.print_error("Blockchain is broken or missing genesis token")
            return False
        self.calculated_balance = utils.check_balance_chain(user_id, ordered_blockchain)
        if self.calculated_balance is False:
            self.calculated_balance = -1
            utils.print_error("Balance cannot be negative")
            return False

        return True

    def merge_chains(self)->None:
        pass
