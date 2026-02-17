from pydantic import BaseModel
from typing import List, Any


class StartConfigResponse(BaseModel):
    activity: str
    id: str
    public_key: str


class FinalConfigRequest(BaseModel):
    id: str
    public_key: str


class LedgerSyncRequest(BaseModel):
    id: str
    blockchain: List[Any]


class SendMoneyRequest(BaseModel):
    id: str
    amount: float
    sender_id: str
    receiver_id: str
