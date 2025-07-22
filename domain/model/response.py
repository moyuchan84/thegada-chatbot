from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class SimpleText(BaseModel):
    text: str

class Thumbnail(BaseModel):
    imageUrl: str

class BasicCard(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    thumbnail: Optional[Thumbnail] = None

class QuickReply(BaseModel):
    label: str
    action: str
    messageText: str

class Component(BaseModel):
    simpleText: Optional[SimpleText] = None
    basicCard: Optional[BasicCard] = None

class SkillTemplate(BaseModel):
    outputs: List[Component]
    quickReplies: Optional[List[QuickReply]] = None

class ContextValue(BaseModel):
    key: str
    value: Any

class ContextControl(BaseModel):
    values: List[ContextValue]
    ttl: int = 10

class Response(BaseModel):
    version: str = "2.0"
    template: SkillTemplate
    context: Optional[ContextControl] = None
