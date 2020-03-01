import json
import mimetypes
import typing as T
from pathlib import Path
from .logger import Network

import aiohttp

from mirai.exceptions import NetworkError

session = aiohttp.ClientSession()

class fetch:
    @staticmethod
    async def http_post(url, data_map):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data_map) as response:
                if response.status != 200:
                    Network.error(f"requested url={url}, by data_map={data_map}, and status={response.status}")
                    raise NetworkError(f"method=POST, url={url}, data={data_map}, status={response.status}")
                data = await response.text(encoding="utf-8")
                Network.debug(f"requested url={url}, by data_map={data_map}, and status={response.status}, data={data}")
        return json.loads(data)

    @staticmethod
    async def http_get(url, params=None): 
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await response.text(encoding="utf-8")
                Network.debug(f"requested url={url}, by params={params}, and status={response.status}, data={data}")
        return json.loads(data)

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
                Network.debug(f"requested url={url}, by filename={file.name}, and status={response.status}, addon_dict={addon_dict}")
                return await response.text("utf-8")