import aiohttp
import typing as T
from pathlib import Path
import mimetypes
import json

class fetch:
    @staticmethod
    async def http_post(url, data_map):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data_map) as response:
                    return await response.json(encoding="utf-8")
        except Exception as e:
            raise e

    @staticmethod
    async def http_get(url, params):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                return await response.json(encoding="utf-8")

    @staticmethod
    async def upload(url, file: Path, addon_dict: dict):
        upload_data = aiohttp.FormData()
        upload_data.add_field("img",
            open(str(file.absolute()), "rb"), filename=file.name
        )
        for item in addon_dict.items():
            upload_data.add_fields(item)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=upload_data) as response:
                return await response.text()