from datetime import datetime
from typing import Union

from pydantic import BaseModel, root_validator

from moragi.models.cj_fresh_meal_response_model import Meal


class Menu(BaseModel):
    detail_info_url: str
    food_type: str
    name: str
    side: str
    thumbnail_url: str
    kcal: int
    status: int

    @classmethod
    def from_cj_meal(cls, cj_fresh_meal_menu_model: Meal):
        CJ_FRESH_MEAL_DETAIL_URL = f'https://front.cjfreshmeal.co.kr/menu/detail/{cj_fresh_meal_menu_model.meal_index}'
        return cls(
            detail_info_url=CJ_FRESH_MEAL_DETAIL_URL,
            food_type=cj_fresh_meal_menu_model.food_type,
            name=cj_fresh_meal_menu_model.name,
            side=cj_fresh_meal_menu_model.side,
            thumbnail_url=cj_fresh_meal_menu_model.thumbnail_url,
            kcal=cj_fresh_meal_menu_model.kcal,
            status=cj_fresh_meal_menu_model.status,
        )


class DailyMenu(BaseModel):
    date: datetime
    breakfast: list[Menu]
    lunch: list[Menu]
    dinner: list[Menu]

    @root_validator
    def check_valid_daily_menu_model(cls, values: dict[str, Union[datetime, list[Menu]]]):
        if not values['breakfast'] and not values['lunch'] and not values['dinner']:
            raise ValueError('No meal has given!')

        return values
