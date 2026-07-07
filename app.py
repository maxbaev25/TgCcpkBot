from dotenv import load_dotenv

load_dotenv()

import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from db import crud
from handlers.registry_handler import router as registry_router
from handlers.info_handler import router as info_router
from handlers.subs_handler import router as subs_router
from scheduler import configure_scheduler, start_scheduler
from aiogram.client.session.aiohttp import AiohttpSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def on_startup(dp: Dispatcher, bot: Bot):
    logging.info('Starting up the bot...')
    await crud.init_all_tables()
    logging.info('All tables initialized.')


async def main():
    dp = Dispatcher()
    dp.include_router(registry_router)
    dp.include_router(info_router)
    dp.include_router(subs_router)

    bot = Bot(token=os.getenv("BOT_TOKEN"), session=AiohttpSession(proxy=os.getenv("PROXY_URL")))

    await configure_scheduler(bot=bot)
    await start_scheduler()

    # dp.startup.register(lambda: asyncio.run(on_startup(dp, bot)))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
