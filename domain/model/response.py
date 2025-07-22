from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Thumbnail(BaseModel):
    imageUrl: str

class BasicCard(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    thumbnail: Thumbnail

class QuickReply(BaseModel):
    label: str
    action: str
    messageText: str

class Component(BaseModel):
    basicCard: BasicCard

class ContextValue(BaseModel):
    key: str
    value: Any

class ContextControl(BaseModel):
    values: List[ContextValue]
    ttl: int = 10 # Time To Live in minutes

class SkillTemplate(BaseModel):
    outputs: List[Component]
    quickReplies: Optional[List[QuickReply]] = None

class Response(BaseModel):
    version: str = "2.0"
    template: SkillTemplate
    context: Optional[ContextControl] = None