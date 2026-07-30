from datetime import datetime
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from db import crud

router = Router()


@router.message(CommandStart())
async def command_start(message: Message):
    current_user = await crud.get_user_by_tg_id(tg_id=message.from_user.id)
    if current_user is not None:
        await message.answer(text="Вы уже зарегистрированы!")
        return
    await crud.create_user(tg_id=message.from_user.id, reg_date=datetime.now())
    await message.answer(text="Вы зарегистрировались!\n"
                              "Введите команду /info для просмотра доступных команд.")
