from datetime import datetime

from pydantic import BaseModel

from moragi.models.cj_fresh_meal_response_model import CJFreshMealMenuModel


class MenuModel(BaseModel):
    detail_info_url: str
    food_type: str
    name: str
    side: str
    thumbnail_url: str
    kcal: int
    status: int

    @classmethod
    def from_cj_fresh_meal_menu_model(cls, cj_fresh_meal_menu_model: CJFreshMealMenuModel):
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


class DailyMenuModel(BaseModel):
    date: datetime
    breakfast: list[MenuModel]
    lunch: list[MenuModel]
    dinner: list[MenuModel]
