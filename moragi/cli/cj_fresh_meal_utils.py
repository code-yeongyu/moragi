import logging

from tenacity import after_log, before_sleep_log, retry, stop_after_attempt, wait_fixed

from moragi.utils import logger
from moragi.utils.cj_fresh_meal import CJFreshMealClient


def get_today_meal(cj_fresh_meal_store_id: int):
    cj_fresh_meal_client = CJFreshMealClient(cj_fresh_meal_store_id)
    daily_menu = cj_fresh_meal_client.get_today_meal()
    return daily_menu


@retry(
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.INFO),
    after=after_log(logger, logging.INFO),
    stop=stop_after_attempt(20),
    wait=wait_fixed(60),
)
def get_menu_with_image(cj_fresh_meal_store_id: int, is_lunch: bool = True):
    daily_menu = get_today_meal(cj_fresh_meal_store_id)
    options = daily_menu.lunch if is_lunch else daily_menu.dinner
    for option in options:
        if not option.thumbnail_url:
            raise Exception('No image found')

    return options
