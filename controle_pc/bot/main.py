import asyncio
from config.config import load_config
from bot.handler import router
from aiogram import Bot, Dispatcher

async def main():
    config = load_config()
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
