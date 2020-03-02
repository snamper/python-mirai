from mirai import Session, Depend, Plain
import asyncio

authKey = "213we355gdfbaerg"
qq = 208924405

async def main():
    async with Session(f"mirai://localhost:8070/?authKey={authKey}&qq={qq}") as session:
        pass