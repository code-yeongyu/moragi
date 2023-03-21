import datetime
import logging
import typing
from typing import Final, Optional

import httpx
from tenacity import after_log, before_sleep_log, retry, stop_after_attempt, wait_fixed

from moragi.models.cj_fresh_meal.response_model import Meal, TodayAllMealResponse, WeekMealResponse
from moragi.models.cj_fresh_meal.week_type import WeekType
from moragi.models.menu import DailyMenu, Menu, WeeklyMenu
from moragi.utils import logger


class CJFreshMealClient:
    BASE_URL = 'https://front.cjfreshmeal.co.kr/meal/v1'

    def __init__(self, store_id: int):
        self.store_id = store_id
        self.client = httpx.Client()

    @retry(
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.DEBUG),
        after=after_log(logger, logging.INFO),
        stop=stop_after_attempt(10),
        wait=wait_fixed(10),
    )
    def get_today_meal(self) -> DailyMenu:
        URL = f'{self.BASE_URL}/today-all-meal?storeIdx={self.store_id}'
        raw_response = self.client.get(URL)
        logger.debug(f'Retrieved Response: {raw_response.json()}')

        response: Final[TodayAllMealResponse] = TodayAllMealResponse.parse_raw(raw_response.text)

        return DailyMenu.from_cj_day_meal(response.meal)

    def _parse_date(self, date: str) -> datetime.datetime:
        return datetime.datetime.strptime(date, '%Y%m%d')

    def _cj_fresh_meal_to_menu(self, cj_fresh_meal_menu_models: Optional[list[Meal]]):
        if cj_fresh_meal_menu_models is None:
            return typing.cast(list[Menu], [])
        return [Menu.from_cj_meal(model) for model in cj_fresh_meal_menu_models]

    @retry(
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.DEBUG),
        after=after_log(logger, logging.DEBUG),
        stop=stop_after_attempt(10),
        wait=wait_fixed(10),
    )
    def get_week_meal(self, week_type: WeekType) -> WeeklyMenu:
        URL = f'{self.BASE_URL}/week-meal?storeIdx={self.store_id}&weekType={week_type.value}'
        raw_response = self.client.get(URL)
        logger.info(f'Retrieved Response: {raw_response.json()}')

        response = WeekMealResponse.parse_raw(raw_response.text)

        return WeeklyMenu.from_cj_week_meal(response.meal)
