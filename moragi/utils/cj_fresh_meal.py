import datetime
import json
import typing
from typing import Final, Optional

import httpx

from moragi.models.cj_fresh_meal.response_model import Meal, TodayAllMealResponse, WeekMealResponse
from moragi.models.cj_fresh_meal.week_type import WeekType
from moragi.models.menu import DailyMenu, Menu, WeeklyMenu
from moragi.utils import console


class CJFreshMealClient:
    BASE_URL = 'https://front.cjfreshmeal.co.kr/meal/v1'

    def __init__(self, store_id: int):
        self.store_id = store_id
        self.client = httpx.Client()

    def get_today_meal(self) -> Optional[DailyMenu]:
        URL = f'{self.BASE_URL}/today-all-meal?storeIdx={self.store_id}'
        console.log(f'Retreving URL: {URL}')

        raw_response = self.client.get(URL)
        console.log('Retrieved Response!', json.dumps(raw_response.text))

        response: Final[TodayAllMealResponse] = TodayAllMealResponse.parse_raw(raw_response.text)

        try:
            return DailyMenu.from_cj_day_meal(response.meal)
        except ValueError:  # if is no meal
            return None

    def _parse_date(self, date: str) -> datetime.datetime:
        return datetime.datetime.strptime(date, '%Y%m%d')

    def _cj_fresh_meal_to_menu(self, cj_fresh_meal_menu_models: Optional[list[Meal]]):
        if cj_fresh_meal_menu_models is None:
            return typing.cast(list[Menu], [])
        return [Menu.from_cj_meal(model) for model in cj_fresh_meal_menu_models]

    def get_week_meal(self, week_type: WeekType) -> Optional[WeeklyMenu]:  # type: ignore
        URL = f'{self.BASE_URL}/week-meal?storeIdx={self.store_id}&weekType={week_type.value}'
        console.log(f'Retreving URL: {URL}')

        raw_response = self.client.get(URL)
        console.log('Retrieved Response!', json.dumps(raw_response.text))

        response = WeekMealResponse.parse_raw(raw_response.text)

        try:
            return WeeklyMenu.from_cj_week_meal(response.meal)
        except ValueError:  # if is no meal
            return None
