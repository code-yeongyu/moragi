import datetime

import httpx
import pytz

from moragi.models.cj_fresh_meal_response_model import CJFreshMealDailyResponseModel, CJFreshMealMenuModel
from moragi.models.menu import DailyMenuModel, MenuModel
from moragi.utils import console


# define the request URL
def get_food_options(store_id: int):
    url = f'https://front.cjfreshmeal.co.kr/meal/v1/today-all-meal?storeIdx={store_id}'
    console.log(f'Retreving URL: {url}')

    with httpx.Client() as client:
        raw_response = client.get(url)
    response = CJFreshMealDailyResponseModel.parse_raw(raw_response.text)

    console.log('Retrieved Response!', response.dict())

    return response.menu


class CJFreshMealClient:
    BASE_URL = 'https://front.cjfreshmeal.co.kr/meal/v1'

    def __init__(self, store_id: int):
        self.store_id = store_id
        self.client = httpx.Client()

    def _cj_fresh_meal_menu_models_to_menu_models(self, cj_fresh_meal_menu_models: list[CJFreshMealMenuModel]):
        return [MenuModel.from_cj_fresh_meal_menu_model(model) for model in cj_fresh_meal_menu_models]

    def get_today_meal(self):
        url = f'{self.BASE_URL}/today-all-meal?storeIdx={self.store_id}'
        console.log(f'Retreving URL: {url}')

        raw_response = self.client.get(url)
        response = CJFreshMealDailyResponseModel.parse_raw(raw_response.text)

        console.log('Retrieved Response!', response.dict())

        breakfast = self._cj_fresh_meal_menu_models_to_menu_models(response.menu.get('1', []))
        lunch = self._cj_fresh_meal_menu_models_to_menu_models(response.menu.get('2', []))
        dinner = self._cj_fresh_meal_menu_models_to_menu_models(response.menu.get('3', []))

        is_no_meal_today = not breakfast and not lunch and not dinner
        if is_no_meal_today:
            return None

        menu = DailyMenuModel(
            date=datetime.datetime.utcnow().astimezone(pytz.timezone('Asia/Seoul')),
            breakfast=breakfast,
            lunch=lunch,
            dinner=dinner,
        )
        return menu

    def get_week_meal(self, week_type: int):  # type: ignore
        _URL = f'{self.BASE_URL}/week-meal?storeIdx={self.store_id}&weekType={week_type}'
        raise NotImplementedError  # todo: implement this
