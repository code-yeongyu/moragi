from time import sleep

from moragi.utils import console
from moragi.utils.cj_fresh_meal import CJFreshMealClient


def get_today_meal(cj_fresh_meal_store_id: int):
    cj_fresh_meal_client = CJFreshMealClient(cj_fresh_meal_store_id)
    daily_menu = cj_fresh_meal_client.get_today_meal()
    if daily_menu is None:
        raise Exception('No meal found for today!')
    return daily_menu


def get_today_lunch_with_image(cj_fresh_meal_store_id: int):
    MAX_TRY = 3
    for i in range(1, MAX_TRY):
        daily_menu = get_today_meal(cj_fresh_meal_store_id)
        lunch_first_option_thumbnail = daily_menu.lunch[0].thumbnail_url
        if lunch_first_option_thumbnail:
            return daily_menu.lunch
        with console.status(f'No image found. Retrying in 10 minutes ... [{i}/{MAX_TRY}]'):
            sleep(60 * 10)
    raise Exception('No image found')
