from typing import Any, Optional
from pydantic import BaseModel

class Chat_Agent_Query(BaseModel):
    context: Any
    query: str
    identifier: Optional[str] = ""
    use_records: bool = True