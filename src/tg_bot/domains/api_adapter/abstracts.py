from abc import ABC, abstractmethod

import httpx


class APIAdapterABC(ABC):
    @abstractmethod
    async def api_post(self, url: str, data: dict | None = None) -> httpx.Response:
        raise NotImplementedError()

    @abstractmethod
    async def api_get(self, url: str, param: dict | None = None) -> httpx.Response:
        raise NotImplementedError()

    @abstractmethod
    async def api_put(self, url: str, data: dict | None = None) -> httpx.Response:
        raise NotImplementedError()

    @abstractmethod
    async def api_patch(self, url: str, data: dict | None = None) -> httpx.Response:
        raise NotImplementedError()

    @abstractmethod
    async def api_delete(self, url: str, params: dict | None = None) -> httpx.Response:
        raise NotImplementedError()
