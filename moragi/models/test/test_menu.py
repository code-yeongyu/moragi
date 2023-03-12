import pytest

from moragi.models.cj_fresh_meal_response_model import Meal
from moragi.models.menu import Menu


@pytest.fixture
def cj_fresh_meal_menu_model():
    cj_fresh_meal_response = {
        'mealIdx': 1,
        'mbrMealIdx': 2,
        'name': 'Test Meal',
        'side': 'Test Side',
        'kcal': 500,
        'carb': 50.0,
        'protein': 20.0,
        'fat': 10.0,
        'salt': 1.0,
        'thumbnailUrl': 'https://example.com/image.jpg',
        'corner': 'Test Food Type',
        'rating': 4,
        'logged': True,
        'loggedAll': False,
        'mealDt': '2022-03-11',
        'status': 1,
        'mealCd': 'Test Code',
        'moHour': '09',
        'tuHour': '09',
        'weHour': '09',
        'thHour': '09',
        'frHour': '09',
        'saHour': '09',
        'suHour': '09',
        'moMinute': '30',
        'tuMinute': '30',
        'weMinute': '30',
        'thMinute': '30',
        'frMinute': '30',
        'saMinute': '30',
        'suMinute': '30',
        'caloriesYn': 'Y'
    }
    return Meal.parse_obj(cj_fresh_meal_response)


def test_menu_model_from_cj_fresh_meal_menu_model(cj_fresh_meal_menu_model: Meal):
    menu_model = Menu.from_cj_meal(cj_fresh_meal_menu_model)

    assert menu_model.detail_info_url == \
        f'https://front.cjfreshmeal.co.kr/menu/detail/{cj_fresh_meal_menu_model.meal_index}'
    assert menu_model.food_type == cj_fresh_meal_menu_model.food_type
    assert menu_model.name == cj_fresh_meal_menu_model.name
    assert menu_model.side == cj_fresh_meal_menu_model.side
    assert menu_model.thumbnail_url == cj_fresh_meal_menu_model.thumbnail_url
    assert menu_model.kcal == cj_fresh_meal_menu_model.kcal
    assert menu_model.status == cj_fresh_meal_menu_model.status
