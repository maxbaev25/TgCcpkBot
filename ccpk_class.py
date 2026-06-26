import pprint
from datetime import date

import requests

from models.sorted_train import SortedTrain
from models.train_places import TrainPlacesObject
from models.unsorted_train import UnsortedTrain

BASE_URL = "https://backend.cppktrain.ru"


def get_all_trains(
        from_station_id: int, to_station_id: int, origin_date: date) -> list[UnsortedTrain] | None:
    url = f"{BASE_URL}/train-schedule/date-travel"
    params = {
        "date": origin_date,
        "fromStationId": from_station_id,
        "toStationId": to_station_id
    }
    try:
        r = requests.get(url, params=params)
        result: list[UnsortedTrain] = []
        for train_dict in r.json():
            result.append(UnsortedTrain.model_validate(train_dict))
        return result
    except Exception as e:
        print(f"An error occurred while completing get_all_trains function:\n{e}")
        return None


def get_all_free_trains(
        from_station_id: int, to_station_id: int, origin_date: date) -> list[SortedTrain] | None:
    url = f"{BASE_URL}/api/TrainPricing"
    params = {
        "departureDate": origin_date.strftime("%Y-%m-%d"),
        "originCode": from_station_id,
        "destinationCode": to_station_id
    }
    try:
        r = requests.get(url, params=params)
        result: list[SortedTrain] = []
        for train_dict in r.json():
            result.append(SortedTrain.model_validate(train_dict))
        return result
    except Exception as e:
        print(f"An error occurred while completing get_all_free_trains function:\n{e}")
        return None


def get_all_train_places(
        train_id: str, from_station_id: str, to_station_id: str, origin_date: date) -> TrainPlacesObject | None:
    url = f"{BASE_URL}/api/CarPricing"
    params = {
        "departuredate": origin_date,
        "origincode": from_station_id,
        "destinationcode": to_station_id,
        "trainnumber": train_id
    }
    try:
        r = requests.get(url, params=params)
        return TrainPlacesObject.model_validate(r.json())
    except Exception as e:
        print(f"An error occurred while completing get_all_train_places function:\n{e}")
        return None
