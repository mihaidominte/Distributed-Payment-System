from fastapi import APIRouter, HTTPException
import time
from database import DatabaseServer
from server_key_store import ServerKeyStore
from tokens_manager import TokensManager
from users_manager import UsersManager
import utils

from app.schemas import (
    FinalConfigRequest,
    LedgerSyncRequest,
    SendMoneyRequest,
)

router = APIRouter()
server_key_store = ServerKeyStore()
server_key_store.load_or_generate()

pending_users = {}


@router.post("/users/start-config")
def new_user_start_config():
    db = DatabaseServer()

    new_user_id = utils.generate_new_user_id()
    pending_users[new_user_id] = time.time()

    return {
        "activity": "config_id",
        "id": new_user_id,
        "public_key": server_key_store.public_key()
    }


@router.post("/users/final-config")
def new_user_final_config(request: FinalConfigRequest):
    db = DatabaseServer()

    if request.id not in pending_users:
        raise HTTPException(status_code=400, detail="invalid_flow")

    new_user = {
        "id": request.id,
        "public_key": request.public_key,
        "balance": 0.0,
        "last_sync": int(time.time())
    }

    if not db.get_one("users", "id = ?", (new_user["id"],)):
        db.insert("users", new_user)
        del pending_users[request.id]
        return {"activity": "success"}

    raise HTTPException(status_code=400, detail="user_exists")


@router.post("/ledger/sync")
def ledger_sync(request: LedgerSyncRequest):
    db = DatabaseServer()
    tokens_manager = TokensManager(db)

    chain_ok = tokens_manager.validate_user_blockchain(request.blockchain)

    if chain_ok:
        new_genesis_token = tokens_manager.generate_genesis_token(request.id)
        return {"activity": "success", "server_token": new_genesis_token}

    raise HTTPException(status_code=400, detail="invalid_chain")


@router.post("/transactions/send")
def send_money(request: SendMoneyRequest):
    db = DatabaseServer()
    users_manager = UsersManager(db)

    if not users_manager.identify_user(request.id):
        raise HTTPException(status_code=401, detail="invalid_user")

    result = users_manager.send_money(
        request.id,
        request.amount,
        request.sender_id,
        request.receiver_id
    )

    if not result:
        raise HTTPException(status_code=400, detail="transfer_failed")

    return {"activity": "success"}
