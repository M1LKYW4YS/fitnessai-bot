from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="register", description="Регистрация"),
        BotCommand(command="profile", description="Мой профиль"),
        BotCommand(command="reset", description="Сбросить профиль")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())