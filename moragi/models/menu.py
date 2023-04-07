from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, root_validator

from moragi.models.cj_fresh_meal import DayMeal, Meal, WeekMeal


class Menu(BaseModel):
    detail_info_url: str
    food_type: str
    name: str
    side: Optional[str]
    thumbnail_url: str
    kcal: int
    status: int

    @property
    def resized_thumbnail_url(self):
        WIDTH = 1200
        return f'https://wsrv.nl/?w={WIDTH}&url={self.thumbnail_url}'

    @classmethod
    def from_cj_meal(cls, cj_fresh_meal: Meal):
        CJ_FRESH_MEAL_DETAIL_URL = f'https://front.cjfreshmeal.co.kr/menu/detail/{cj_fresh_meal.meal_index}'
        return cls(
            detail_info_url=CJ_FRESH_MEAL_DETAIL_URL,
            food_type=cj_fresh_meal.food_type,
            name=cj_fresh_meal.name,
            side=cj_fresh_meal.side,
            thumbnail_url=cj_fresh_meal.thumbnail_url,
            kcal=cj_fresh_meal.kcal,
            status=cj_fresh_meal.status,
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

    @classmethod
    def from_cj_day_meal(cls, cj_fresh_day_meal: DayMeal):

        def parse_date(date: str) -> datetime:
            return datetime.strptime(date, '%Y%m%d')

        menu_date: datetime
        if cj_fresh_day_meal.breakfast:
            menu_date = parse_date(cj_fresh_day_meal.breakfast[0].meal_date)
        elif cj_fresh_day_meal.lunch:
            menu_date = parse_date(cj_fresh_day_meal.lunch[0].meal_date)
        elif cj_fresh_day_meal.dinner:
            menu_date = parse_date(cj_fresh_day_meal.dinner[0].meal_date)
        else:
            raise ValueError('No meal has given!')

        return cls(
            date=menu_date,
            breakfast=[Menu.from_cj_meal(meal) for meal in cj_fresh_day_meal.breakfast or []],
            lunch=[Menu.from_cj_meal(meal) for meal in cj_fresh_day_meal.lunch or []],
            dinner=[Menu.from_cj_meal(meal) for meal in cj_fresh_day_meal.dinner or []],
        )


class WeeklyMenu(BaseModel):
    monday: Optional[DailyMenu]
    tuesday: Optional[DailyMenu]
    wednesday: Optional[DailyMenu]
    thursday: Optional[DailyMenu]
    friday: Optional[DailyMenu]
    saturday: Optional[DailyMenu]
    sunday: Optional[DailyMenu]

    @root_validator
    def check_valid_weekly_menu_model(cls, values: dict[str, Optional[DailyMenu]]):
        is_everyday_empty = not values['monday'] \
                        and not values['tuesday'] \
                        and not values['wednesday'] \
                        and not values['thursday'] \
                        and not values['friday'] \
                        and not values['saturday'] \
                        and not values['sunday']
        if is_everyday_empty:
            raise ValueError('WeeklyMenu has at least one day menu!')

        return values

    @classmethod
    def from_cj_week_meal(cls, cj_fresh_week_meal: WeekMeal):

        def from_cj_day_meal(cj_fresh_day_meal: DayMeal):
            try:
                return DailyMenu.from_cj_day_meal(cj_fresh_day_meal)
            except ValueError:
                return None

        return cls(
            monday=\
                from_cj_day_meal(cj_fresh_week_meal.monday) if cj_fresh_week_meal.monday else None,
            tuesday=\
                from_cj_day_meal(cj_fresh_week_meal.tuesday) if cj_fresh_week_meal.tuesday else None,
            wednesday=\
                from_cj_day_meal(cj_fresh_week_meal.wednesday) if cj_fresh_week_meal.wednesday else None,
            thursday=\
                from_cj_day_meal(cj_fresh_week_meal.thursday) if cj_fresh_week_meal.thursday else None,
            friday=\
                from_cj_day_meal(cj_fresh_week_meal.friday) if cj_fresh_week_meal.friday else None,
            saturday=\
                from_cj_day_meal(cj_fresh_week_meal.saturday) if cj_fresh_week_meal.saturday else None,
            sunday=\
                from_cj_day_meal(cj_fresh_week_meal.sunday) if cj_fresh_week_meal.sunday else None,
        )
