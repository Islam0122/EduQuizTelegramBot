import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from dotenv import find_dotenv, load_dotenv

from database.engine import drop_db, create_db, session_maker
from database.orm_query import orm_get_id_bot_user, orm_add_admin
from handlers.admin_panel.start_admin import admin_private_router
from handlers.user_panel.start_functions import start_functions_private_router

from middlewares.db import DataBaseSession
from common.bot_cmds_list import private

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'))
bot.my_admins_list = [5627082052, ]
bot.group_id = os.getenv('group_id')
dp = Dispatcher()

dp.include_router(admin_private_router)
dp.include_router(start_functions_private_router)


async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_db()
    await create_db()


    async with session_maker() as session:
        users = await orm_get_id_bot_user(session)
        for admin_id in bot.my_admins_list:
            if admin_id not in users:
                await orm_add_admin(session, user_id=admin_id, name="Islam", username="@admin")


    # Отправляем сообщение первому администратору
    await bot.send_message(bot.my_admins_list[0], "Сервер успешно запущен! 😊 Привет, босс!")


async def on_shutdown(bot):
    await bot.send_message(bot.my_admins_list[0], "Сервер остановлен. 😔 Проверьте его состояние, босс!")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())
