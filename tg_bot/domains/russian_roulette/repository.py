from dataclasses import dataclass

from app.users.schemas import UsersCreateSchema
from tg_bot.domains.api_adapter.service import APIAdapter
from tg_bot.domains.russian_roulette.schemas import BadPhraseMessage


@dataclass
class RussianRouletteRepository:
    api_adapter: APIAdapter

    async def start(self, user_data: UsersCreateSchema) -> BadPhraseMessage:
        register_suer_result = await self.api_adapter.api_post(
            "/russian_roulette/",
            data=user_data.model_dump(mode="json"),
        )
        resp = register_suer_result.json()
        if resp.get("detail"):
            raise Exception(resp["detail"])
        return BadPhraseMessage(phrase=resp.get("phrase"))
