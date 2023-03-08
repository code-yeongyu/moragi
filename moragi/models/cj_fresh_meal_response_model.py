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
    corner: str
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


class CJFreshMealResponse(BaseModel):
    status: str
    return_code: str = Field(alias='retCode')
    return_message: str = Field(alias='retMsg')
    date: str
    meals: dict[str, list[Meal]] = Field(alias='data')
