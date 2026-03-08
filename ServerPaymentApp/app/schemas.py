from pydantic import BaseModel


class RequestCreateUser(BaseModel):
    public_key: str

class RequestGenerateTokens(BaseModel):
    public_key: str
    amount: int

