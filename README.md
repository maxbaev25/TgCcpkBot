*Будущая структура проекта:*

*Файлы:*\
app.py\312
loader.py\
ccpk_class.py\
checking_scheduler.py

*Директории:*\
handlers\
keyboards\
states\
db

*Описание файлов:*\
app.py - файл для запуска бота\
loader.py - добавление роутеров в диспетчера\
ccpk_class.py - класс с api-функциями для получения данных\
checking_scheduler.py - файл с APScheduler, проверяющий наличие мест

*Описание директорий:*\
handlers - нужна для хранения в ней handler'ов\
keyboards - хранение inline-клавиатур и callback_data для них\
states - хранение состояний\
db - содержит crud, models и engine

*Структура базы данных:*\

*Таблицы:*\
1) users - для хранения авторизованных пользователей
2) subscriptions - для хранения подписок пользователей на рассылку о свободных местах

*Структура:*\
1) users\
id INTEGER PRIMARY KEY AUTOINCREMENT
tg_id INTEGER
regdate DATETIME (registration_date)
2) subscriptions\
id INTEGER PRIMARY KEY AUTOINCREMENT
user_id INTEGER
from_station_id INTEGER
to_station_id INTEGER
origin_date DATETIME
