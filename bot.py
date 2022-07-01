import aiogram.types
from aiogram import Bot
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types

import config
import db


storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print('Bot is running')
    db.start_db()


@dp.message_handler(commands='start')
async def strt(message: types.Message):
    await bot.send_message(message.from_user.id, text="Welcome!\n"
                                                      "To learn all the features of the bot type: /help\n\n"
                                                      f"Your user ID: {message.from_user.id}\n"
                                                      f"--------------------------------------------------------------------------\n\n"
                                                      f"Добро пожаловать!\n"
                                                      f"Чтобы узнать все возможности бота наберите: /help")
    if db.db_user(message.from_user.id) == None:
        await db.db_add(message.from_user.id, message.from_user.first_name, message.from_user.last_name)



@dp.message_handler(commands='help')
async def hlp(message: types.Message):
    await bot.send_message(message.from_user.id, text="This bot was created so that you can find out your ID,\n"
                                                      "find out the ID of the chat and the person from the forwarded message\n\n"
                                                      "Just send the right message HERE\n"
                                                      "And you will receive all the information\n\n"
                                                      "----------------------------------------------------------------------------------------\n\n"
                                                      "Этот бот создан для того, чтобы вы могли узнать свой ID,\n"
                                                      "узнать ID чата и человека из пересланного сообщения\n\n"
                                                      "Просто отправьте правильное сообщение ЗДЕСЬ\n"
                                                      "И вы получите всю информацию")



@dp.message_handler(filters.ForwardedMessageFilter(is_forwarded=True), content_types=aiogram.types.ContentType.ANY)
async def forw_mess_id(message: types.Message):
    if message.forward_from_chat:
        await bot.send_message(message.from_user.id, text="Message info:\n"
                                                          f"Channel ID: {message.forward_from_chat.id}\n"
                                                          f"Channel Username: @{message.forward_from_chat.username}\n"
                                                          f"Title: {message.forward_from_chat.title}")
    else:
        try:
            await bot.send_message(message.from_user.id, text="Message info:\n"
                                                      f"User ID: {message.forward_from.id}\n"
                                                      f"Username: @{message.forward_from.username}\n"
                                                      f"First Name: {message.forward_from.first_name}")
        except Exception:
            await bot.send_message(message.from_user.id, text="This account is hidden by the user.\n\n"
                                                              "The user must write to the bot himself!\n"
                                                              "----------------------------------------------------------------------------------------\n\n"
                                                              "Эта учетная запись скрыта пользователем.\n\n"
                                                              "Пользователь должен сам написать боту!")


@dp.message_handler()
async def mess_id(message: types.Message):
    await bot.send_message(message.from_user.id, text="Message info:\n"
                                                     f"User ID: {message.from_user.id}\n"
                                                     f"Username: @{message.from_user.username}\n"
                                                     f"First Name: {message.from_user.first_name}")



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)