
from pydantic import BaseModel
from typing import Optional

class UserRequest(BaseModel):
    utterance: str
    user: dict

class Request(BaseModel):
    userRequest: UserRequest
    bot: dict
    action: dict
    contexts: list = []
