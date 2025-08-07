from dataclasses import dataclass

import httpx

from src.tg_bot.core.api_adapter.abstracts import APIAdapterABC


@dataclass
class APIAdapter(APIAdapterABC):
    base_url: str = "http://localhost:8000"

    async def api_post(self, url: str, data: dict | None = None) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url + url, json=data)
            if response.status_code == 409:
                return response
            response.raise_for_status()
            return response

    async def api_get(self, url: str, param: dict | None = None) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url + url, params=param)
            return response

    async def api_put(self, url: str, data: dict | None = None) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.put(self.base_url + url, json=data)
            response.raise_for_status()
            return response

    async def api_patch(self, url: str, data: dict | None = None) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.patch(self.base_url + url, json=data)
            response.raise_for_status()
            return response

    async def api_delete(self, url: str, params: dict | None = None) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.delete(self.base_url + url, params=params)
            response.raise_for_status()
            return response
