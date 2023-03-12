from typing import Optional

from pydantic import BaseModel, Field


class Meal(BaseModel):
    meal_index: int = Field(alias='mealIdx')
    mbr_meal_idx: int = Field(alias='mbrMealIdx')
    name: str
    side: str
    kcal: int
    carb: float
    protein: float
    fat: float
    salt: float
    thumbnail_url: str = Field(alias='thumbnailUrl')
    food_type: str = Field(alias='corner')
    rating: int
    logged: bool
    logged_all: bool = Field(alias='loggedAll')
    meal_date: str = Field(alias='mealDt')
    status: int
    meal_code: str = Field(alias='mealCd')
    mo_hour: str = Field(alias='moHour')
    tu_hour: str = Field(alias='tuHour')
    we_hour: str = Field(alias='weHour')
    th_hour: str = Field(alias='thHour')
    fr_hour: str = Field(alias='frHour')
    sa_hour: str = Field(alias='saHour')
    su_hour: str = Field(alias='suHour')
    mo_minute: str = Field(alias='moMinute')
    tu_minute: str = Field(alias='tuMinute')
    we_minute: str = Field(alias='weMinute')
    th_minute: str = Field(alias='thMinute')
    fr_minute: str = Field(alias='frMinute')
    sa_minute: str = Field(alias='saMinute')
    su_minute: str = Field(alias='suMinute')
    calories_yn: str = Field(alias='caloriesYn')

    class Config:
        allow_population_by_field_name = True


class DayMeal(BaseModel):
    breakfast: Optional[list[Meal]] = Field(alias='1')
    lunch: Optional[list[Meal]] = Field(alias='2')
    dinner: Optional[list[Meal]] = Field(alias='3')

    class Config:
        allow_population_by_field_name = True


class WeekMeal(BaseModel):
    monday: Optional[DayMeal] = Field(alias='mo')
    tuesday: Optional[DayMeal] = Field(alias='tu')
    wednesday: Optional[DayMeal] = Field(alias='we')
    thursday: Optional[DayMeal] = Field(alias='th')
    friday: Optional[DayMeal] = Field(alias='fr')
    saturday: Optional[DayMeal] = Field(alias='sa')
    sunday: Optional[DayMeal] = Field(alias='su')

    class Config:
        allow_population_by_field_name = True


class TodayAllMealResponse(BaseModel):
    '''The response of `today-all-meal` API'''
    status: str
    return_code: str = Field(alias='retCode')
    return_message: str = Field(alias='retMsg')
    date: str  # in format of: 20230307
    meal: DayMeal = Field(alias='data')

    class Config:
        allow_population_by_field_name = True


class WeekMealResponse(BaseModel):
    '''The response of `week-meal` API'''
    status: str
    return_code: str = Field(alias='retCode')
    return_message: str = Field(alias='retMsg')
    date: str
    meal: WeekMeal = Field(alias='data')

    class Config:
        allow_population_by_field_name = True
