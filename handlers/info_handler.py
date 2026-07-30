from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from db import crud

router = Router()


@router.message(Command('info'))
async def command_info(message: Message):
    current_user = await crud.get_user_by_tg_id(tg_id=message.from_user.id)
    if current_user is None:
        await message.answer(text="Вы не зарегистрированы!\n"
                                  "Введите команду /start для регистрации.")
        return
    await message.answer(text="Список доступных команд:\n"
                              "/info - выводит информацию о доступных командах\n"
                              "/my_subs - выводит информацию о ваших подписках\n"
                              "/sub - позволяет оформить подписку\n"
                              "/unsub - позволяет отменить подписку\n"
                              "/unsub_all - позволяет отменить все подписки")
