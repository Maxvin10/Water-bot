from aiogram import types, Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
from handlers import router
import asyncio
import config
import logging

bot = Bot(token=config.TOKEN)

dp = Dispatcher()


async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_router(router)
    await bot.set_my_commands([
        BotCommand(command = "/start", description="Botni ishga tushirish"),
        BotCommand(command =  "/help", description="Yordam"),
        BotCommand(command = "/menu", description="Xarid qilish")
    ])
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
