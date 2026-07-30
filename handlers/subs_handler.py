from datetime import datetime
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from db import crud

router = Router()


@router.message(Command("my_subs"))
async def command_my_subs(message: Message):
    current_user = await crud.get_user_by_tg_id(tg_id=message.from_user.id)
    if current_user is None:
        await message.answer(text="Вы не зарегистрированы!\n"
                                  "Введите команду /start для регистрации.")
        return
    user_subs = await crud.get_all_user_subs_by_user_tg_id(user_tg_id=current_user.tg_id)
    if user_subs is None:
        await message.answer(text="Ошибка при получении подписок, обратитесь в поддержку.")
        return
    if len(user_subs) == 0:
        await message.answer(text="У вас пока нет подписок!\n"
                                  "Используйте команду /sub для подписки.")
        return
    # s = sub
    lines = [
        f"{num}) {s.origin_date.date()}: {s.from_station_id} -> {s.to_station_id}"
        for num, s in enumerate(user_subs)
    ]
    await message.answer(text="Список ваших подписок:\n" + '\n'.join(lines))


@router.message(Command("sub"))
async def command_sub(message: Message, cmd: CommandObject):
    current_user = await crud.get_user_by_tg_id(tg_id=message.from_user.id)
    if current_user is None:
        await message.answer(text="Вы не зарегистрированы!\n"
                                  "Введите команду /start для регистрации.")
        return
    parts = cmd.args.split() if cmd.args else []
    # parts[0] - from, parts[1] - to, parts[2] - date(по умолчанию на завтра)
    error_text = "Требуется команда вида /sub from_station_id to_station_id date(по умолчанию завтра)"
    try:
        from_station_id, to_station_id, origin_date = parse_sub_command(parts=parts)
    except ValueError:
        await message.answer(text=error_text)
        return
    await crud.create_sub_by_user_tg_id(
        user_tg_id=current_user.tg_id,
        to_station_id=to_station_id,
        from_station_id=from_station_id,
        origin_date=origin_date)
    await message.answer(text="Подписка успешно добавлена!")


@router.message(Command("unsub"))
async def command_unsub(message: Message, cmd: CommandObject):
    current_user = await crud.get_user_by_tg_id(tg_id=message.from_user.id)
    if current_user is None:
        await message.answer(text="Вы не зарегистрированы!\n"
                                  "Введите команду /start для регистрации.")
        return
    parts = cmd.args.split() if cmd.args else []
    # parts[0] - from, parts[1] - to, parts[2] - date(по умолчанию на завтра)
    error_text = "Требуется команда вида /unsub from_station_id to_station_id date(по умолчанию завтра)"
    try:
        from_station_id, to_station_id, origin_date = parse_sub_command(parts=parts)
    except ValueError:
        await message.answer(text=error_text)
        return
    sub = await crud.get_sub(
        to_station_id=from_station_id,
        from_station_id=to_station_id,
        origin_date=origin_date,
        user_id=current_user.id)
    if sub is None:
        await message.answer(text="У вас нет такой подписки!")
        return
    await crud.delete_sub_by_sub_id(sub_id=sub.id)
    await message.answer(text="Подписка успешно удалена!")


@router.message(Command("unsub_all"))
async def command_unsub(message: Message):
    current_user = await crud.get_user_by_tg_id(tg_id=message.from_user.id)
    if current_user is None:
        await message.answer(text="Вы не зарегистрированы!\n"
                                  "Введите команду /start для регистрации.")
        return
    await crud.delete_all_user_subs_by_user_tg_id(user_tg_id=current_user.tg_id)
    await message.answer(text="Вы успешно отписались от всех подписок!")


def parse_sub_command(parts: list):
    if len(parts) < 2:
        raise ValueError
    try:
        from_id, to_id = int(parts[0]), int(parts[1])
    except ValueError as e:
        raise ValueError from e
    origin_date = None
    if len(parts) >= 3:
        try:
            origin_date = datetime.strptime(parts[2], "%Y-%m-%d")
        except ValueError:
            pass
    if origin_date is None:
        origin_date = datetime.now()
    return from_id, to_id, origin_date
