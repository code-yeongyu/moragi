from unittest import mock
from unittest.mock import MagicMock, patch

import pytest

from moragi.models.cj_fresh_meal.week_type import WeekType
from moragi.models.menu import Menu
from moragi.utils.cj_fresh_meal import CJFreshMealClient


@pytest.fixture
def cj_fresh_meal_client():
    return CJFreshMealClient(1000)


class TestGetTodayMeal:

    @mock.patch('httpx.Client.get')
    def test_get_today_meal__no_meal(
        self,
        mock_get: MagicMock,
        cj_fresh_meal_client: CJFreshMealClient,
    ):
        # given
        sample_response_text = '''
        {
            "status": "success",
            "retCode": "00",
            "retMsg": "",
            "date": "Sun Mar 12 18:25:20 KST 2023",
            "data": {}
        }
        '''
        mock_get.return_value.text = sample_response_text

        # when
        today_menu = cj_fresh_meal_client.get_today_meal()

        # then
        assert today_menu is None

    @mock.patch('httpx.Client.get')
    @pytest.mark.parametrize('meal_type', ['1', '2', '3'])
    def test_get_today_meal__only_one_meal(
        self,
        mock_get: MagicMock,
        meal_type: str,
        cj_fresh_meal_client: CJFreshMealClient,
    ):
        # given
        sample_response_text = '''
        {
            "status": "success",
            "retCode": "0",
            "retMsg": "",
            "data": {
                "meal_type": [
                    {
                        "mealIdx": 1,
                        "mbrMealIdx": 0,
                        "name": "Egg Sandwich",
                        "side": "",
                        "kcal": 289,
                        "carb": 38.8,
                        "protein": 12.9,
                        "fat": 8.6,
                        "salt": 2.2,
                        "thumbnailUrl": "https://example.com/example.jpeg",
                        "corner": "TAKE OUT",
                        "rating": 0,
                        "logged": false,
                        "loggedAll": false,
                        "mealDt": "20220314",
                        "status": 1,
                        "mealCd": "F",
                        "moHour": "",
                        "tuHour": "",
                        "weHour": "",
                        "thHour": "",
                        "frHour": "",
                        "saHour": "",
                        "suHour": "",
                        "moMinute": "",
                        "tuMinute": "",
                        "weMinute": "",
                        "thMinute": "",
                        "frMinute": "",
                        "saMinute": "",
                        "suMinute": "",
                        "caloriesYn": "N"
                    }
                ]
            },
            "date": "2022-03-14"
        }
        '''
        sample_response_text = sample_response_text.replace('meal_type', meal_type)
        mock_get.return_value.text = sample_response_text

        # when
        today_menu = cj_fresh_meal_client.get_today_meal()

        # then
        assert today_menu is not None
        assert today_menu.date.strftime('%Y-%m-%d') == '2022-03-14'

        today_menu_data: list[Menu] = []
        if meal_type == '1':
            assert today_menu.breakfast
            today_menu_data = today_menu.breakfast
        elif meal_type == '2':
            assert today_menu.lunch
            today_menu_data = today_menu.lunch
        elif meal_type == '3':
            assert today_menu.dinner
            today_menu_data = today_menu.dinner

        assert today_menu_data
        assert today_menu_data[0].name == 'Egg Sandwich'
        assert today_menu_data[0].kcal == 289
        assert today_menu_data[0].status == 1


class TestGetWeekMeal:

    @patch('httpx.Client.get')
    @pytest.mark.parametrize('week_type', [WeekType.THIS_WEEK, WeekType.NEXT_WEEK])
    def test_success__get_week_meal(
        self,
        mocked_get: MagicMock,
        week_type: WeekType,
        cj_fresh_meal_client: CJFreshMealClient,
    ):
        # given
        sample_response_text = '''
        {
            "status": "success",
            "retCode": "00",
            "retMsg": "",
            "date": "Sun Mar 12 18:18:36 KST 2023",
            "data": {
                "tu": {
                "1": [
                    {
                    "mealIdx": 500028,
                    "mbrMealIdx": 0,
                    "name": "플레인베이글*크림치즈",
                    "side": "+사이드, 음료 1종",
                    "kcal": 445,
                    "carb": 0,
                    "protein": 0,
                    "fat": 0,
                    "salt": 0,
                    "thumbnailUrl": "https://example.com/example.jpeg",
                    "corner": "TAKE OUT",
                    "rating": 0,
                    "logged": false,
                    "loggedAll": false,
                    "mealDt": "20230307",
                    "status": 1,
                    "mealCd": "1",
                    "moHour": "10",
                    "tuHour": "10",
                    "weHour": "10",
                    "thHour": "10",
                    "frHour": "10",
                    "saHour": "10",
                    "suHour": "10",
                    "moMinute": "50",
                    "tuMinute": "50",
                    "weMinute": "50",
                    "thMinute": "50",
                    "frMinute": "50",
                    "saMinute": "50",
                    "suMinute": "50",
                    "caloriesYn": "Y"
                    }
                ],
                "2": [
                    {
                    "mealIdx": 500009,
                    "mbrMealIdx": 0,
                    "name": "양지설렁탕&소면사리",
                    "side": "쌀밥, 오징어김치전, 탕평채, 오이쌈장무침, 그린샐러드, 깍두기",
                    "kcal": 814,
                    "carb": 0,
                    "protein": 0,
                    "fat": 0,
                    "salt": 0,
                    "thumbnailUrl": "https://example.com/example.jpeg",
                    "corner": "백반",
                    "rating": 0,
                    "logged": false,
                    "loggedAll": false,
                    "mealDt": "20230307",
                    "status": 1,
                    "mealCd": "2",
                    "moHour": "14",
                    "tuHour": "14",
                    "weHour": "14",
                    "thHour": "14",
                    "frHour": "14",
                    "saHour": "14",
                    "suHour": "14",
                    "moMinute": "50",
                    "tuMinute": "50",
                    "weMinute": "50",
                    "thMinute": "50",
                    "frMinute": "50",
                    "saMinute": "50",
                    "suMinute": "50",
                    "caloriesYn": "Y"
                    },
                    {
                    "mealIdx": 500016,
                    "mbrMealIdx": 0,
                    "name": "게살푸팟퐁커리&갈릭버터난",
                    "side": "쌀국수장국, 동남아식 레몬치킨, 망고라씨, 그린샐러드, 깍두기",
                    "kcal": 723,
                    "carb": 0,
                    "protein": 0,
                    "fat": 0,
                    "salt": 0,
                    "thumbnailUrl": "https://example.com/example.jpeg",
                    "corner": "스페셜",
                    "rating": 0,
                    "logged": false,
                    "loggedAll": false,
                    "mealDt": "20230307",
                    "status": 1,
                    "mealCd": "2",
                    "moHour": "14",
                    "tuHour": "14",
                    "weHour": "14",
                    "thHour": "14",
                    "frHour": "14",
                    "saHour": "14",
                    "suHour": "14",
                    "moMinute": "50",
                    "tuMinute": "50",
                    "weMinute": "50",
                    "thMinute": "50",
                    "frMinute": "50",
                    "saMinute": "50",
                    "suMinute": "50",
                    "caloriesYn": "Y"
                    },
                    {
                    "mealIdx": 500035,
                    "mbrMealIdx": 0,
                    "name": "에그쉬림프 샐러드/크랜베리치킨 샌드위치",
                    "side": "+사이드, 음료 1종",
                    "kcal": 391,
                    "carb": 0,
                    "protein": 0,
                    "fat": 0,
                    "salt": 0,
                    "thumbnailUrl": "https://example.com/example.jpeg",
                    "corner": "TAKE OUT",
                    "rating": 0,
                    "logged": false,
                    "loggedAll": false,
                    "mealDt": "20230307",
                    "status": 1,
                    "mealCd": "2",
                    "moHour": "14",
                    "tuHour": "14",
                    "weHour": "14",
                    "thHour": "14",
                    "frHour": "14",
                    "saHour": "14",
                    "suHour": "14",
                    "moMinute": "50",
                    "tuMinute": "50",
                    "weMinute": "50",
                    "thMinute": "50",
                    "frMinute": "50",
                    "saMinute": "50",
                    "suMinute": "50",
                    "caloriesYn": "Y"
                    }
                ]
                },
                "mo": {
                "1": [],
                "2": [
                    {
                    "mealIdx": 500004,
                    "mbrMealIdx": 0,
                    "name": "부채살스테이크&더운야채",
                    "side": "트러플머쉬룸스프, 갈릭필라프, 토마토리가토니파스타, 보코치니과일샐러드, 수제비트무피클, 배추김치, 마카롱",
                    "kcal": 1233,
                    "carb": 0,
                    "protein": 0,
                    "fat": 0,
                    "salt": 0,
                    "thumbnailUrl": "https://example.com/example.jpeg",
                    "corner": "백반",
                    "rating": 0,
                    "logged": false,
                    "loggedAll": false,
                    "mealDt": "20230306",
                    "status": 1,
                    "mealCd": "2",
                    "moHour": "14",
                    "tuHour": "14",
                    "weHour": "14",
                    "thHour": "14",
                    "frHour": "14",
                    "saHour": "14",
                    "suHour": "14",
                    "moMinute": "50",
                    "tuMinute": "50",
                    "weMinute": "50",
                    "thMinute": "50",
                    "frMinute": "50",
                    "saMinute": "50",
                    "suMinute": "50",
                    "caloriesYn": "Y"
                    }
                ]
                },
                "su": {
                "1": [],
                "2": []
                },
                "th": {
                "1": [
                    {
                    "mealIdx": 500022,
                    "mbrMealIdx": 0,
                    "name": "던킨도넛 레인보우초코링",
                    "side": "+사이드, 음료 1종",
                    "kcal": 523,
                    "carb": 0,
                    "protein": 0,
                    "fat": 0,
                    "salt": 0,
                    "thumbnailUrl": "https://example.com/example.jpeg",
                    "corner": "TAKE OUT",
                    "rating": 0,
                    "logged": false,
                    "loggedAll": false,
                    "mealDt": "20230309",
                    "status": 1,
                    "mealCd": "1",
                    "moHour": "10",
                    "tuHour": "10",
                    "weHour": "10",
                    "thHour": "10",
                    "frHour": "10",
                    "saHour": "10",
                    "suHour": "10",
                    "moMinute": "50",
                    "tuMinute": "50",
                    "weMinute": "50",
                    "thMinute": "50",
                    "frMinute": "50",
                    "saMinute": "50",
                    "suMinute": "50",
                    "caloriesYn": "Y"
                    }
                ],
                "2": [
                    {
                    "mealIdx": 500006,
                    "mbrMealIdx": 0,
                    "name": "닭보쌈구이*파채겉절이",
                    "side": "쌀밥, 순두부찌개, 비빔막국수, 무말랭이무침, 콘코울슬로, 배추김치",
                    "kcal": 890,
                    "carb": 0,
                    "protein": 0,
                    "fat": 0,
                    "salt": 0,
                    "thumbnailUrl": "https://example.com/example.jpeg",
                    "corner": "백반",
                    "rating": 0,
                    "logged": false,
                    "loggedAll": false,
                    "mealDt": "20230309",
                    "status": 1,
                    "mealCd": "2",
                    "moHour": "14",
                    "tuHour": "14",
                    "weHour": "14",
                    "thHour": "14",
                    "frHour": "14",
                    "saHour": "14",
                    "suHour": "14",
                    "moMinute": "50",
                    "tuMinute": "50",
                    "weMinute": "50",
                    "thMinute": "50",
                    "frMinute": "50",
                    "saMinute": "50",
                    "suMinute": "50",
                    "caloriesYn": "Y"
                    },
                    {
                    "mealIdx": 500019,
                    "mbrMealIdx": 0,
                    "name": "통등심돈까스*만다린샐러드",
                    "side": "배추김치, 후리가께밥, 우동장국, 분모자매콤떡볶이, 콘코울슬로",
                    "kcal": 916,
                    "carb": 0,
                    "protein": 0,
                    "fat": 0,
                    "salt": 0,
                    "thumbnailUrl": "https://example.com/example.jpeg",
                    "corner": "스페셜",
                    "rating": 0,
                    "logged": false,
                    "loggedAll": false,
                    "mealDt": "20230309",
                    "status": 1,
                    "mealCd": "2",
                    "moHour": "14",
                    "tuHour": "14",
                    "weHour": "14",
                    "thHour": "14",
                    "frHour": "14",
                    "saHour": "14",
                    "suHour": "14",
                    "moMinute": "50",
                    "tuMinute": "50",
                    "weMinute": "50",
                    "thMinute": "50",
                    "frMinute": "50",
                    "saMinute": "50",
                    "suMinute": "50",
                    "caloriesYn": "Y"
                    },
                    {
                    "mealIdx": 500013,
                    "mbrMealIdx": 0,
                    "name": "청포도리코타치즈 샐러드/크로와상햄치즈 샌드위치",
                    "side": "+사이드, 음료 1종",
                    "kcal": 396,
                    "carb": 0,
                    "protein": 0,
                    "fat": 0,
                    "salt": 0,
                    "thumbnailUrl": "https://example.com/example.jpeg",
                    "corner": "TAKE OUT",
                    "rating": 0,
                    "logged": false,
                    "loggedAll": false,
                    "mealDt": "20230309",
                    "status": 1,
                    "mealCd": "2",
                    "moHour": "14",
                    "tuHour": "14",
                    "weHour": "14",
                    "thHour": "14",
                    "frHour": "14",
                    "saHour": "14",
                    "suHour": "14",
                    "moMinute": "50",
                    "tuMinute": "50",
                    "weMinute": "50",
                    "thMinute": "50",
                    "frMinute": "50",
                    "saMinute": "50",
                    "suMinute": "50",
                    "caloriesYn": "Y"
                    }
                ]
                },
                "fr": {
                "1": [
                    {
                    "mealIdx": 500010,
                    "mbrMealIdx": 0,
                    "name": "부시맨브레드*이즈니버터",
                    "side": "+사이드, 음료 1종",
                    "kcal": 368,
                    "carb": 0,
                    "protein": 0,
                    "fat": 0,
                    "salt": 0,
                    "thumbnailUrl": "https://example.com/example.jpeg",
                    "corner": "TAKE OUT",
                    "rating": 0,
                    "logged": false,
                    "loggedAll": false,
                    "mealDt": "20230310",
                    "status": 1,
                    "mealCd": "1",
                    "moHour": "10",
                    "tuHour": "10",
                    "weHour": "10",
                    "thHour": "10",
                    "frHour": "10",
                    "saHour": "10",
                    "suHour": "10",
                    "moMinute": "50",
                    "tuMinute": "50",
                    "weMinute": "50",
                    "thMinute": "50",
                    "frMinute": "50",
                    "saMinute": "50",
                    "suMinute": "50",
                    "caloriesYn": "Y"
                    }
                ],
                "2": [
                    {
                    "mealIdx": 500032,
                    "mbrMealIdx": 0,
                    "name": "얼큰낙차새전골",
                    "side": "쌀밥, 비엔나케찹볶음, 단호박부꾸미, 부추무침, 누룽지샐러드, 배추김치",
                    "kcal": 721,
                    "carb": 0,
                    "protein": 0,
                    "fat": 0,
                    "salt": 0,
                    "thumbnailUrl": "https://example.com/example.jpeg",
                    "corner": "백반",
                    "rating": 0,
                    "logged": false,
                    "loggedAll": false,
                    "mealDt": "20230310",
                    "status": 1,
                    "mealCd": "2",
                    "moHour": "14",
                    "tuHour": "14",
                    "weHour": "14",
                    "thHour": "14",
                    "frHour": "14",
                    "saHour": "14",
                    "suHour": "14",
                    "moMinute": "50",
                    "tuMinute": "50",
                    "weMinute": "50",
                    "thMinute": "50",
                    "frMinute": "50",
                    "saMinute": "50",
                    "suMinute": "50",
                    "caloriesYn": "Y"
                    },
                    {
                    "mealIdx": 500034,
                    "mbrMealIdx": 0,
                    "name": "중화짜장밥*계란후라이",
                    "side": "게살스프, 찹쌀꿔바로우, 단무지, 누룽지샐러드, 배추김치",
                    "kcal": 750,
                    "carb": 0,
                    "protein": 0,
                    "fat": 0,
                    "salt": 0,
                    "thumbnailUrl": "https://example.com/example.jpeg",
                    "corner": "스페셜",
                    "rating": 0,
                    "logged": false,
                    "loggedAll": false,
                    "mealDt": "20230310",
                    "status": 1,
                    "mealCd": "2",
                    "moHour": "14",
                    "tuHour": "14",
                    "weHour": "14",
                    "thHour": "14",
                    "frHour": "14",
                    "saHour": "14",
                    "suHour": "14",
                    "moMinute": "50",
                    "tuMinute": "50",
                    "weMinute": "50",
                    "thMinute": "50",
                    "frMinute": "50",
                    "saMinute": "50",
                    "suMinute": "50",
                    "caloriesYn": "Y"
                    },
                    {
                    "mealIdx": 500018,
                    "mbrMealIdx": 0,
                    "name": "프로틴업 샐러드/키토소시지 김밥",
                    "side": "+사이드, 음료 1종",
                    "kcal": 386,
                    "carb": 0,
                    "protein": 0,
                    "fat": 0,
                    "salt": 0,
                    "thumbnailUrl": "https://example.com/example.jpeg",
                    "corner": "TAKE OUT",
                    "rating": 0,
                    "logged": false,
                    "loggedAll": false,
                    "mealDt": "20230310",
                    "status": 1,
                    "mealCd": "2",
                    "moHour": "14",
                    "tuHour": "14",
                    "weHour": "14",
                    "thHour": "14",
                    "frHour": "14",
                    "saHour": "14",
                    "suHour": "14",
                    "moMinute": "50",
                    "tuMinute": "50",
                    "weMinute": "50",
                    "thMinute": "50",
                    "frMinute": "50",
                    "saMinute": "50",
                    "suMinute": "50",
                    "caloriesYn": "Y"
                    }
                ]
                },
                "we": {
                "1": [
                    {
                    "mealIdx": 500025,
                    "mbrMealIdx": 0,
                    "name": "아이돌샌드위치",
                    "side": "+사이드, 음료 1종",
                    "kcal": 726,
                    "carb": 0,
                    "protein": 0,
                    "fat": 0,
                    "salt": 0,
                    "thumbnailUrl": "https://example.com/example.jpeg",
                    "corner": "TAKE OUT",
                    "rating": 0,
                    "logged": false,
                    "loggedAll": false,
                    "mealDt": "20230308",
                    "status": 2,
                    "mealCd": "1",
                    "moHour": "10",
                    "tuHour": "10",
                    "weHour": "10",
                    "thHour": "10",
                    "frHour": "10",
                    "saHour": "10",
                    "suHour": "10",
                    "moMinute": "50",
                    "tuMinute": "50",
                    "weMinute": "50",
                    "thMinute": "50",
                    "frMinute": "50",
                    "saMinute": "50",
                    "suMinute": "50",
                    "caloriesYn": "Y"
                    }
                ],
                "2": [
                    {
                    "mealIdx": 500007,
                    "mbrMealIdx": 0,
                    "name": "직화쭈꾸미불고기*콩나물찜",
                    "side": "쌀밥, 소고기미역국, 카레고로케, 깻잎*쌈무*날치알마요, 양배추샐러드, 배추김치",
                    "kcal": 886,
                    "carb": 0,
                    "protein": 0,
                    "fat": 0,
                    "salt": 0,
                    "thumbnailUrl": "https://example.com/example.jpeg",
                    "corner": "백반",
                    "rating": 0,
                    "logged": false,
                    "loggedAll": false,
                    "mealDt": "20230308",
                    "status": 1,
                    "mealCd": "2",
                    "moHour": "14",
                    "tuHour": "14",
                    "weHour": "14",
                    "thHour": "14",
                    "frHour": "14",
                    "saHour": "14",
                    "suHour": "14",
                    "moMinute": "50",
                    "tuMinute": "50",
                    "weMinute": "50",
                    "thMinute": "50",
                    "frMinute": "50",
                    "saMinute": "50",
                    "suMinute": "50",
                    "caloriesYn": "Y"
                    },
                    {
                    "mealIdx": 500020,
                    "mbrMealIdx": 0,
                    "name": "텐동",
                    "side": "유부미소시루, 토마토유자절임, 락교&초생강, 양배추샐러드, 배추김치",
                    "kcal": 785,
                    "carb": 0,
                    "protein": 0,
                    "fat": 0,
                    "salt": 0,
                    "thumbnailUrl": "https://example.com/example.jpeg",
                    "corner": "스페셜",
                    "rating": 0,
                    "logged": false,
                    "loggedAll": false,
                    "mealDt": "20230308",
                    "status": 1,
                    "mealCd": "2",
                    "moHour": "14",
                    "tuHour": "14",
                    "weHour": "14",
                    "thHour": "14",
                    "frHour": "14",
                    "saHour": "14",
                    "suHour": "14",
                    "moMinute": "50",
                    "tuMinute": "50",
                    "weMinute": "50",
                    "thMinute": "50",
                    "frMinute": "50",
                    "saMinute": "50",
                    "suMinute": "50",
                    "caloriesYn": "Y"
                    },
                    {
                    "mealIdx": 500033,
                    "mbrMealIdx": 0,
                    "name": "케이준치킨 샐러드/스팸김치 컵밥",
                    "side": "+사이드, 음료 1종",
                    "kcal": 561,
                    "carb": 0,
                    "protein": 0,
                    "fat": 0,
                    "salt": 0,
                    "thumbnailUrl": "https://example.com/example.jpeg",
                    "corner": "TAKE OUT",
                    "rating": 0,
                    "logged": false,
                    "loggedAll": false,
                    "mealDt": "20230308",
                    "status": 2,
                    "mealCd": "2",
                    "moHour": "14",
                    "tuHour": "14",
                    "weHour": "14",
                    "thHour": "14",
                    "frHour": "14",
                    "saHour": "14",
                    "suHour": "14",
                    "moMinute": "50",
                    "tuMinute": "50",
                    "weMinute": "50",
                    "thMinute": "50",
                    "frMinute": "50",
                    "saMinute": "50",
                    "suMinute": "50",
                    "caloriesYn": "Y"
                    }
                ]
                },
                "sa": {
                "1": [],
                "2": []
                }
            }
        }
        '''
        mocked_get.return_value.text = sample_response_text

        # when
        weekly_menu = cj_fresh_meal_client.get_week_meal(week_type)

        # then
        assert weekly_menu is not None
        assert weekly_menu.monday
        assert weekly_menu.tuesday
        assert weekly_menu.wednesday
        assert weekly_menu.thursday
        assert weekly_menu.friday
        assert weekly_menu.saturday is None
        assert weekly_menu.sunday is None

    @patch('httpx.Client.get')
    @pytest.mark.parametrize('week_type', [WeekType.THIS_WEEK, WeekType.NEXT_WEEK])
    def test_fail__get_week_meal_empty(
        self,
        mocked_get: MagicMock,
        week_type: WeekType,
        cj_fresh_meal_client: CJFreshMealClient,
    ):
        # given
        sample_response_text = '''
        {
            "status": "success",
            "retCode": "00",
            "retMsg": "",
            "date": "Sun Mar 12 18:18:36 KST 2023",
            "data": {
                "mo": {
                    "1": [],
                    "2": []
                },
                "tu": {
                    "1": [],
                    "2": []
                },
                "we": {
                    "1": [],
                    "2": []
                },
                "th": {
                    "1": [],
                    "2": []
                },
                "fr": {
                    "1": [],
                    "2": []
                },
                "sa": {
                    "1": [],
                    "2": []
                },
                "su": {
                    "1": [],
                    "2": []
                }
            }
        }
        '''
        mocked_get.return_value.text = sample_response_text

        # when
        weekly_menu = cj_fresh_meal_client.get_week_meal(week_type)

        # then
        assert weekly_menu is None

    @patch('httpx.Client.get')
    @pytest.mark.parametrize('week_type', [WeekType.THIS_WEEK, WeekType.NEXT_WEEK])
    def test_fail__get_week_meal_data_empty(
        self,
        mocked_get: MagicMock,
        week_type: WeekType,
        cj_fresh_meal_client: CJFreshMealClient,
    ):
        # given
        sample_response_text = '''
        {
            "status": "success",
            "retCode": "00",
            "retMsg": "",
            "date": "Sun Mar 12 18:18:36 KST 2023",
            "data": {}
        }
        '''
        mocked_get.return_value.text = sample_response_text

        # when
        weekly_menu = cj_fresh_meal_client.get_week_meal(week_type)

        # then
        assert weekly_menu is None
