from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import uuid
import hashlib
import traceback

def calculate_token_hash(previous_hash: str, sender_id: str, receiver_id: str, amount: float, date: int) -> str:
    data = f"{previous_hash}|{sender_id}|{receiver_id}|{amount}|{date}"
    return hashlib.sha256(data.encode()).hexdigest()

def calculate_genesis_token_hash(sender_id: str, receiver_id: str, amount: float, date: int) -> str:
    data = f"{sender_id}|{receiver_id}|{amount}|{date}"
    return hashlib.sha256(data.encode()).hexdigest()

def generate_new_id()->str:
    return str(uuid.uuid4())

def generate_new_user_id()->str:
    return generate_new_id()

def sign_hash(hash_value: str, server_private_key) -> str:
    signature_bytes = server_private_key.sign(
        hash_value.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return base64.b64encode(signature_bytes).decode()

def check_sign(hash_value: str, signature, public_key) -> bool:
    try:
        signature_bytes = base64.b64decode(signature)
        public_key.verify(
            signature_bytes,
            hash_value.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    except Exception as e:
        print(f"[VERIFY ERROR] {e}")
        return False

def check_owner_chain(owner_id: str, blockchain: list[dict]) -> bool:
    for t in blockchain:
        if t["user_id"] != owner_id:
            return False
        if t["sender_id"] != owner_id and t["receiver_id"] != owner_id:
            return False
    return True

def check_token_integrity(token: dict) -> bool:
    previous_hash = token["previous_hash"]
    if previous_hash is None:
        genesis_calculated_hash = calculate_genesis_token_hash(
            token["sender_id"], token["receiver_id"], token["amount"], token["date"])
        if genesis_calculated_hash != token["hash"]:
            return False
    else:
        token_calculated_hash = calculate_token_hash(
            token["previous_hash"], token["sender_id"], token["receiver_id"], token["amount"], token["date"])
        if token_calculated_hash != token["hash"]:
            return False
    return True

def rebuild_chain(blockchain: list[dict]) -> list[dict] | bool:
    genesis_tokens = [t for t in blockchain if t["previous_hash"] is None]
    if len(genesis_tokens) != 1:
        return False

    genesis = genesis_tokens[0]

    by_prev = {t["previous_hash"]: t for t in blockchain if t["previous_hash"] is not None}

    ordered = [genesis]
    current = genesis
    visited = {genesis["hash"]}

    while current["hash"] in by_prev:
        next_token = by_prev[current["hash"]]

        if next_token["hash"] in visited:
            return False

        ordered.append(next_token)
        visited.add(next_token["hash"])
        current = next_token

    if len(ordered) != len(blockchain):
        return False

    return ordered


def check_balance_chain(user_id: str, ordered_blockchain: list[dict]) -> float | bool:
    balance = 0.0
    for t in ordered_blockchain:
        if t["sender_id"] == user_id:
            balance -= t["amount"]
        elif t["receiver_id"] == user_id:
            balance += t["amount"]
        if balance < 0:
            return False
    return balance


def print_error(msg: str):
    print(f"\033[91m[ERROR] {msg}\033[0m")
    traceback.print_exc()

"""Send money online activity"""
"""check_owner_token = utils.check_owner_chain(
            message["user_id"], [message["genesis_token"]])
        if check_owner_token:
            check_token_integrity = utils.check_token_integrity(message["genesis_token"])
            if check_token_integrity:
                check_token_server_sign = utils.check_sign(
                    message["genesis_token"]["hash"], message["genesis_token"]["counter_sig"], server_public_key)
                user_public_key = db.get_one(
                    "users", "user_id = ?", (message["user_id"],))["public_key"]
                check_token_user_sign = utils.check_sign(
                    message["genesis_token"]["hash"], message["genesis_token"]["signature"], user_public_key)
                if check_token_server_sign and check_token_user_sign:
                    pass
                else:
                    utils.print_error("Token signature check failed")
                    return {"activity": "fail"}
            else:
                utils.print_error("Token integrity check failed")
                return {"activity": "fail"}
        else:
            utils.print_error("Token owner check failed")
            return {"activity": "fail"}"""

"""Receive money online activity"""

