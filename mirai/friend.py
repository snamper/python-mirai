from uuid import UUID
from pydantic import BaseModel
from typing import Optional

class Friend(BaseModel):
    id: int
    nickname: Optional[str]
    remark: Optional[str]

    def __repr__(self):
        return f"<Friend id={self.id} nickname='{self.nickname}' remark='{self.remark}'>"
