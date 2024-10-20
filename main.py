import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.utils import exceptions
from aiogram.utils.exceptions import ChatNotFound
from config import BOT_TOKEN, GROUP_ID
from database import init_db, add_user, update_user_registration, is_user_registered

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Клавиатура для регистрации
registration_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
registration_keyboard.add(KeyboardButton("Зарегистрироваться на мероприятие"))

# Справочная информация
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer("Это бот для регистрации на вебинар. Нажмите кнопку 'Зарегистрироваться', чтобы начать.")

# Стартовое сообщение
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await add_user(message.from_user.id)
    await message.answer("Добро пожаловать! Хотите зарегистрироваться на вебинар?", reply_markup=registration_keyboard)

# Регистрация на мероприятие
@dp.message_handler(lambda message: message.text == "Зарегистрироваться на мероприятие")
async def register_for_event(message: types.Message):
    user_id = message.from_user.id
    is_registered = await is_user_registered(user_id)

    if is_registered:
        await message.answer("Вы уже зарегистрированы! Вот ваша ссылка на мероприятие: https://example.com/event")
    else:
        await message.answer(f"Пожалуйста, вступите в нашу группу: https://t.me/joinchat/{GROUP_ID}")
        await message.answer("После вступления нажмите кнопку снова для завершения регистрации.")

# Повторная проверка подписки и завершение регистрации
@dp.message_handler(lambda message: message.text == "Я вступил в группу")
async def check_group_and_register(message: types.Message):
    user_id = message.from_user.id
    try:
        chat_member = await bot.get_chat_member(GROUP_ID, user_id)
        if chat_member.status in ['member', 'administrator', 'creator']:
            await update_user_registration(user_id)
            await message.answer("Регистрация завершена! Вот ваша ссылка на мероприятие: https://example.com/event")
        else:
            await message.answer("Пожалуйста, сначала вступите в группу!")
    except ChatNotFound:
        await message.answer("Ошибка! Проверьте ссылку на группу.")

if __name__ == '__main__':
    from aiogram import executor
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    executor.start_polling(dp, skip_updates=True)
