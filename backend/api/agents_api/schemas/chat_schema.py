from typing import Optional
from pydantic import BaseModel

class Chat_Agent_Query(BaseModel):
    query: str
    identifier: Optional[str] = ""