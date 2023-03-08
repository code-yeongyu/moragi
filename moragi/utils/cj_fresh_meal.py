import httpx

from moragi.models.cj_fresh_meal_response_model import CJFreshMealResponse
from moragi.utils import console


# define the request URL
def get_food_options(store_id: int):
    url = f'https://front.cjfreshmeal.co.kr/meal/v1/today-all-meal?storeIdx={store_id}'
    console.log(f'Retreving URL: {url}')

    with httpx.Client() as client:
        raw_response = client.get(url)
    response = CJFreshMealResponse.parse_raw(raw_response.text)

    console.log('Retrieved Response!', response.dict())

    return response.meals
