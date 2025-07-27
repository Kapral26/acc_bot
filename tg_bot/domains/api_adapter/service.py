
import httpx

from tg_bot.domains.api_adapter.abstracts import APIAdapterABC


class APIAdapter(APIAdapterABC):

    async def api_post(self, url: str, data: dict | None = None) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            if response.status_code == 409:
                return response
            response.raise_for_status()
            return response

    async def api_get(self, url: str, param: dict | None = None) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=param)
            response.raise_for_status()
            return response

    async def api_put(self, url: str, data: dict | None = None) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.put(url, json=data)
            response.raise_for_status()
            return response

    async def api_patch(self, url: str, data: dict | None = None) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.patch(url, json=data)
            response.raise_for_status()
            return response

    async def api_delete(self, url: str, params: dict | None = None) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, params=params)
            response.raise_for_status()
            return response
