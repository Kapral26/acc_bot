import asyncio

from tg_bot.bot_app import TelegramBot

if __name__ == "__main__":
    bot = TelegramBot()
    asyncio.run(bot.main())

