from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from mirai.network import session
from PIL import Image
from io import BytesIO

class Friend(BaseModel):
    id: int
    nickname: Optional[str]
    remark: Optional[str]

    def __repr__(self):
        return f"<Friend id={self.id} nickname='{self.nickname}' remark='{self.remark}'>"

    def getAvatarUrl(self) -> str:
        return f'http://q4.qlogo.cn/g?b=qq&nk={self.id}&s=140'

    async def getAvatarAsPillowImage(self) -> Image.Image:
        async with session.get(self.getAvatarUrl()) as response:
            return Image.open(BytesIO(await response.read()))