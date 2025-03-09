import asyncio,os
from config.config import load_config
from bot.handler import router
try:
    from aiogram import Bot, Dispatcher
except:
    os.system("python -m pip install aiogram")
    from aiogram import Bot, Dispatcher
config = load_config()
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())