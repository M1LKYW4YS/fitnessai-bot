import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from bot.config import BOT_TOKEN
from bot.handlers import start, register, profile
from bot.set_commands import set_bot_commands

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начать"),
        BotCommand(command="register", description="Регистрация"),
        BotCommand(command="profile", description="Посмотреть профиль"),
        BotCommand(command="reset", description="Сбросить профиль")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        start.router,
        register.router,
        profile.router
    )

    await set_bot_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())