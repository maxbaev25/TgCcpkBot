from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from aiogram import Bot
from db import crud
import logging
from ccpk_class import *
from models.train_places import TrainPlacesObject
from db.models import Subscription, User

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


def process_trains(free_trains: list, user: User, sub: Subscription) -> list[str]:
    message_lines = [
        f"Подписка пользователя {user.id} на {sub.from_station_id} -> {sub.to_station_id} ({sub.origin_date.date()}):"
    ]
    for train in free_trains:
        train_places = get_all_train_places(
            to_station_id=train.destinationStationCode,
            from_station_id=train.originStationCode,
            origin_date=train.departureDateTime,
            train_id=train.trainNumber
        )
        if train_places is None:
            continue
        message_lines.extend(process_train_places(train, train_places))
    return message_lines


def process_train_places(train, train_places) -> list[str]:
    message_lines = [
        f"Кол-во свободных мест в поезде {train.trainNumber} в {train.departureDateTime.strftime('%H:%M')}:"
    ]
    for place in train_places.trainPlaces:
        message_lines.append(
            f"{place.displayName}: всего {place.places.total} мест по {int(place.price)} руб."
        )
        car_lines = [f"Вагон {car.number}: {car.placeQuantity} места" for car in place.cars]
        message_lines.extend(car_lines)
    return message_lines


async def process_subscription(user: User, sub: Subscription, bot: Bot):
    free_trains = get_all_free_trains(
        to_station_id=sub.to_station_id,
        from_station_id=sub.from_station_id,
        origin_date=sub.origin_date.date()
    )
    if not free_trains:
        logger.info(f"Нет свободных поездов для подписки {sub.id}")
        return
    message_lines = process_trains(free_trains, user, sub)
    if message_lines:
        full_message = "\n".join(message_lines)
        logger.info(full_message)
        # await bot.send_message(chat_id=user.tg_id, text=full_message)


async def process_subs(user: User, subs: list[Subscription], bot: Bot):
    for sub in subs:
        await process_subscription(user, sub, bot)


async def check_all_users(bot: Bot):
    users = await crud.get_all_users()
    for user in users:
        subs = await crud.get_all_user_subs_by_user_tg_id(user_tg_id=user.tg_id)
        if subs is None:
            continue
        await process_subs(user=user, subs=subs, bot=bot)


async def configure_scheduler(bot: Bot, check_interval: int = 900):
    trigger = IntervalTrigger(seconds=check_interval)
    scheduler.add_job(
        check_all_users,
        trigger=trigger,
        args=[bot],
        max_instances=1,
        replace_existing=True
    )
    await check_all_users(bot=bot)
    logger.info("Scheduler configured")


async def stop_scheduler():
    scheduler.shutdown()
    logger.info("Scheduler stopped")


async def start_scheduler():
    scheduler.start()
    logging.info("Scheduler started")
