from pydantic import BaseModel
from typing import Optional
from langchain_core.messages import BaseMessage

class User(BaseModel):
    username: str
    email: str
    password: str

class DisplayUser(BaseModel):
    username: str
    email: str
    # class Config:
    #     orm_mode = True # Deprecated in Pydantic v2
    model_config = {"from_attributes": True} # Correct for Pydantic v2

class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None

class AllThreads(BaseModel):
    threads: list[str]

class RequestThreadID(BaseModel):
    thread_id: str

class AllMessages(BaseModel):
    messages: list[BaseMessage]

class RequestMsg(BaseModel):
    msg: str
    thread_id: str

class ResultMsg(BaseModel):
    res: str
