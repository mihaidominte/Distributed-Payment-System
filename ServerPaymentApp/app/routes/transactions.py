from fastapi import APIRouter, HTTPException
from database import DatabaseServer
from app.schemas import RequestGenerateTokens
from tokens_manager import TokensManager


router = APIRouter()

@router.post("/transactions/get-tokens")
def get_tokens(request: RequestGenerateTokens):
    db = DatabaseServer()
    user = db.get_one("users", "public_key = ?", (request.public_key,))

    if user is not None:
        tokens_manager = TokensManager()
        tokens = tokens_manager.generate_tokens(RequestGenerateTokens.amount, user.id)
        return tokens

    raise HTTPException(status_code=400, detail="user_unknown")

@router.post("/transactions/send-tokens")
def send_tokens(tokens):
    pass