import datetime

import requests
from pprint import pprint, pp
from datetime import datetime, date

BASE_URL = "https://backend.cppktrain.ru


def get_all_trains(
        from_station_id: int, to_station_id: int, origin_date: date) -> list[dict]:
    url = f"{BASE_URL}/train-schedule/date-travel"
    params = {
        "date": origin_date,
        "fromStationId": from_station_id,
        "toStationId": to_station_id
    }
    try:
        r = requests.get(url, params=params)
        return r.json()
    except:
        print("Ошибка")
    return None


def get_all_free_trains(
        from_station_id: int, to_station_id: int, origin_date: date) -> list[dict]:
    url = f"{BASE_URL}/api/TrainPricing"
    params = {
        "departureDate": origin_date.strftime("%Y-%m-%d"),
        "originCode": from_station_id,
        "destinationCode": to_station_id
    }
    r = requests.get(url, params=params)
    return r.json()


def get_all_train_places(
        train_id: int, from_station_id: int, to_station_id: int, origin_date: date) -> dict:
    url = f"{BASE_URL}/api/CarPricing"
    params = {
        "departuredate": "2026-06-11",
        "origincode": from_station_id,
        "destinationcode": to_station_id,
        "trainnumber": train_id
    }
    r = requests.get(url, params=params)
    return r.json()


for t in get_all_free_trains(
        from_station_id=2000001, to_station_id=2000880, origin_date=date(year=2026, month=6, day=12)):
    train_places = get_all_train_places(
        train_id=t["trainNumber"],
        from_station_id=t["route"]["originStation"]["code"],
        to_station_id=t["route"]["destinationStation"]["code"],
        origin_date=datetime.strptime(t["route"]["departureDateTime"],
                                      "%Y-%m-%dT%H:%M:%S").date())
    for place in train_places["trainPlaces"]:
        # pp(place)
        print("--------")
        pp(int(place["price"]))
        pp(place["places"]["total"])
        pp(place["displayName"])
