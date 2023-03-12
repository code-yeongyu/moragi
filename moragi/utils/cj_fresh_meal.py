import datetime
import json
import typing
from typing import Optional

import httpx

from moragi.models.cj_fresh_meal_response_model import Meal, TodayAllMealResponse
from moragi.models.menu import DailyMenu, Menu
from moragi.utils import console


class CJFreshMealClient:
    BASE_URL = 'https://front.cjfreshmeal.co.kr/meal/v1'

    def __init__(self, store_id: int):
        self.store_id = store_id
        self.client = httpx.Client()

    def _cj_fresh_meal_menu_models_to_menu_models(self, cj_fresh_meal_menu_models: Optional[list[Meal]]):
        if cj_fresh_meal_menu_models is None:
            return typing.cast(list[Menu], [])
        return [Menu.from_cj_meal(model) for model in cj_fresh_meal_menu_models]

    def _parse_date(self, date: str) -> datetime.datetime:
        return datetime.datetime.strptime(date, '%Y%m%d')

    def get_today_meal(self) -> Optional[DailyMenu]:
        url = f'{self.BASE_URL}/today-all-meal?storeIdx={self.store_id}'
        console.log(f'Retreving URL: {url}')

        raw_response = self.client.get(url)
        console.log('Retrieved Response!', json.dumps(raw_response.text))

        response = TodayAllMealResponse.parse_raw(raw_response.text)
        breakfast = self._cj_fresh_meal_menu_models_to_menu_models(response.meal.breakfast)
        lunch = self._cj_fresh_meal_menu_models_to_menu_models(response.meal.lunch)
        dinner = self._cj_fresh_meal_menu_models_to_menu_models(response.meal.dinner)
        menu_date: datetime.datetime
        if response.meal.breakfast:
            menu_date = self._parse_date(response.meal.breakfast[0].meal_date)
        elif response.meal.lunch:
            menu_date = self._parse_date(response.meal.lunch[0].meal_date)
        elif response.meal.dinner:
            menu_date = self._parse_date(response.meal.dinner[0].meal_date)
        else:  # if is no meal
            return None

        try:
            daily_menu = DailyMenu(
                date=menu_date,
                breakfast=breakfast,
                lunch=lunch,
                dinner=dinner,
            )
            return daily_menu
        except ValueError:  # if is no meal
            return None

    def get_week_meal(self, week_type: int):  # type: ignore
        _URL = f'{self.BASE_URL}/week-meal?storeIdx={self.store_id}&weekType={week_type}'
        raise NotImplementedError  # todo: implement this
