from uuid import UUID

class Friend:
    id: int
    nickname: str
    remark: str

    @classmethod
    def parser(cls, info_map):
        friend = cls()
        friend.id = info_map['id']
        friend.nickname = info_map['nickName']
        friend.remark = info_map['remark']
        return friend

    def __repr__(self):
        return f"<Friend id={self.id} nickname='{self.nickname}' remark='{self.remark}'>"

    def imageRender(self, imageId: UUID):
        return f"{{{str(imageId).upper()}}}."