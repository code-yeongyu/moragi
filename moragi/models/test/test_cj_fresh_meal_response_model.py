import json

from moragi.models.cj_fresh_meal_response_model import DayMeal


def test_parse_day_menu_model():
    # given
    day_menu_response = json.dumps({
        '1': [{
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
        }]
    })

    # when
    day_meal = DayMeal.parse_raw(day_menu_response)

    # then
    assert day_meal.breakfast is not None
    assert day_meal.lunch is None
    assert day_meal.dinner is None
