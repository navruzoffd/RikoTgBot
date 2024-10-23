from typing import Optional
from pydantic import BaseModel


class UserData(BaseModel):
    hash: Optional[str] = None
    telegramId: int
    photo: Optional[str] = ""
    username: str
    premium: Optional[bool] = False


class CheckChatMemberResponse(BaseModel):
    success: bool
    result: bool
    

class CheckChatMemberRequest(BaseModel):
    chat_id: int
    telegram_id: int
    hash: Optional[str] = None
