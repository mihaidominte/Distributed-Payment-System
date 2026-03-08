import uuid
from fastapi import APIRouter, HTTPException
from database import DatabaseServer
from server_key_store import ServerKeyCertificate

from app.schemas import RequestCreateUser

router = APIRouter()
server_key_certificate = ServerKeyCertificate()


@router.post("/users/create-user")
def create_user(request: RequestCreateUser):
    """Noii utilizatori sunt validati aici
    Acestia trebuie sa isi trimita cheia publica pentru a fi validata
    Daca cheia exista deja cererea va fi respinsa
    Daca utilizatorul prezinta o cheie noua, va primi certificatul aferent si cheia publica a
    serverului pentru a verifica alti useri
    In viitor aici noul utilizator va trimite si date de identitate care vor fi verificate si stocate ca garantie"""

    db = DatabaseServer()

    if not db.get_one("users", "public_key = ?", (request.public_key,)):
        certificate = server_key_certificate.sign(request.public_key)
        server_public_key = server_key_certificate.public_key()
        new_user = {
            "id": str(uuid.uuid4()),
            "public_key": request.public_key
        }
        db.insert("users", new_user)

        return {"activity": "success", "certificate": certificate, "server_public_key": server_public_key}

    raise HTTPException(status_code=400, detail="user_exists")
