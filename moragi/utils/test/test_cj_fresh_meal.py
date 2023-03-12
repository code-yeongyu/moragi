from unittest import mock
from unittest.mock import MagicMock

import pytest

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
        mock_response_text = '''
        {
            "status": "success",
            "retCode": "0",
            "retMsg": "",
            "data": {
                "meal_type": []
            },
            "date": "2022-03-14"
        }
        '''
        mock_get.return_value.text = mock_response_text

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
        mock_response_text = '''
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
                        "thumbnailUrl": "test_url",
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
        mock_response_text = mock_response_text.replace('meal_type', meal_type)
        mock_get.return_value.text = mock_response_text

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


# @patch('httpx.Client.get')
# def test_success__get_week_meal(mocked_get: MagicMock):
#     # given
#     sample_response = {
#         'status': 'success',
#         'retCode': '00',
#         'retMsg': '',
#         'date': 'Sun Mar 12 15:49:53 KST 2023',
#         'data': {
#             'tu': {
#                 '1': [{
#                     'mealIdx': 500028,
#                     'mbrMealIdx': 0,
#                     'name': '플레인베이글*크림치즈',
#                     'side': '+사이드, 음료 1종',
#                     'kcal': 445.0,
#                     'carb': 0.0,
#                     'protein': 0.0,
#                     'fat': 0.0,
#                     'salt': 0.0,
#                     'thumbnailUrl': '',
#                     'corner': 'TAKE OUT',
#                     'rating': 0,
#                     'logged': False,
#                     'loggedAll': False,
#                     'mealDt': '20230307',
#                     'status': 1,
#                     'mealCd': '1',
#                     'moHour': '10',
#                     'tuHour': '10',
#                     'weHour': '10',
#                     'thHour': '10',
#                     'frHour': '10',
#                     'saHour': '10',
#                     'suHour': '10',
#                     'moMinute': '50',
#                     'tuMinute': '50',
#                     'weMinute': '50',
#                     'thMinute': '50',
#                     'frMinute': '50',
#                     'saMinute': '50',
#                     'suMinute': '50',
#                     'caloriesYn': 'Y'
#                 }],
#                 '2': [{
#                     'mealIdx': 500009,
#                     'mbrMealIdx': 0,
#                     'name': '양지설렁탕&소면사리',
#                     'side': '쌀밥, 오징어김치전, 탕평채, 오이쌈장무침, 그린샐러드, 깍두기',
#                     'kcal': 814.0,
#                     'carb': 0.0,
#                     'protein': 0.0,
#                     'fat': 0.0,
#                     'salt': 0.0,
#                     'thumbnailUrl': '20230307_eBm_1678155504882.jpeg',
#                     'corner': '백반',
#                     'rating': 0,
#                     'logged': False,
#                     'loggedAll': False,
#                     'mealDt': '20230307',
#                     'status': 1,
#                     'mealCd': '2',
#                     'moHour': '14',
#                     'tuHour': '14',
#                     'weHour': '14',
#                     'thHour': '14',
#                     'frHour': '14',
#                     'saHour': '14',
#                     'suHour': '14',
#                     'moMinute': '50',
#                     'tuMinute': '50',
#                     'weMinute': '50',
#                     'thMinute': '50',
#                     'frMinute': '50',
#                     'saMinute': '50',
#                     'suMinute': '50',
#                     'caloriesYn': 'Y'
#                 }, {
#                     'mealIdx': 500016,
#                     'mbrMealIdx': 0,
#                     'name': '게살푸팟퐁커리&갈릭버터난',
#                     'side': '쌀국수장국, 동남아식 레몬치킨, 망고라씨, 그린샐러드, 깍두기',
#                     'kcal': 723.0,
#                     'carb': 0.0,
#                     'protein': 0.0,
#                     'fat': 0.0,
#                     'salt': 0.0,
#                     'thumbnailUrl': '20230307_SLj_1678155513049.jpeg',
#                     'corner': '스페셜',
#                     'rating': 0,
#                     'logged': False,
#                     'loggedAll': False,
#                     'mealDt': '20230307',
#                     'status': 1,
#                     'mealCd': '2',
#                     'moHour': '14',
#                     'tuHour': '14',
#                     'weHour': '14',
#                     'thHour': '14',
#                     'frHour': '14',
#                     'saHour': '14',
#                     'suHour': '14',
#                     'moMinute': '50',
#                     'tuMinute': '50',
#                     'weMinute': '50',
#                     'thMinute': '50',
#                     'frMinute': '50',
#                     'saMinute': '50',
#                     'suMinute': '50',
#                     'caloriesYn': 'Y'
#                 }, {
#                     'mealIdx': 500035,
#                     'mbrMealIdx': 0,
#                     'name': '에그쉬림프 샐러드/크랜베리치킨 샌드위치',
#                     'side': '+사이드, 음료 1종',
#                     'kcal': 391.0,
#                     'carb': 0.0,
#                     'protein': 0.0,
#                     'fat': 0.0,
#                     'salt': 0.0,
#                     'thumbnailUrl': 'aab49535-c8d8-44df-a98a-aa4e5f53072c_99A0C0DF-0BE8-4DAF-8667-42CE80E25B1B.jpeg',
#                     'corner': 'TAKE OUT',
#                     'rating': 0,
#                     'logged': False,
#                     'loggedAll': False,
#                     'mealDt': '20230307',
#                     'status': 1,
#                     'mealCd': '2',
#                     'moHour': '14',
#                     'tuHour': '14',
#                     'weHour': '14',
#                     'thHour': '14',
#                     'frHour': '14',
#                     'saHour': '14',
#                     'suHour': '14',
#                     'moMinute': '50',
#                     'tuMinute': '50',
#                     'weMinute': '50',
#                     'thMinute': '50',
#                     'frMinute': '50',
#                     'saMinute': '50',
#                     'suMinute': '50',
#                     'caloriesYn': 'Y'
#                 }]
#             },
#             'mo': {
#                 '1': [],
#                 '2': [{
#                     'mealIdx': 500004,
#                     'mbrMealIdx': 0,
#                     'name': '부채살스테이크&더운야채',
#                     'side': '트러플머쉬룸스프, 갈릭필라프, 토마토리가토니파스타, 보코치니과일샐러드, 수제비트무피클, 배추김치, 마카롱',
#                     'kcal': 1233.0,
#                     'carb': 0.0,
#                     'protein': 0.0,
#                     'fat': 0.0,
#                     'salt': 0.0,
#                     'thumbnailUrl': '20230306_TWK_1678068133449.jpeg',
#                     'corner': '백반',
#                     'rating': 0,
#                     'logged': False,
#                     'loggedAll': False,
#                     'mealDt': '20230306',
#                     'status': 1,
#                     'mealCd': '2',
#                     'moHour': '14',
#                     'tuHour': '14',
#                     'weHour': '14',
#                     'thHour': '14',
#                     'frHour': '14',
#                     'saHour': '14',
#                     'suHour': '14',
#                     'moMinute': '50',
#                     'tuMinute': '50',
#                     'weMinute': '50',
#                     'thMinute': '50',
#                     'frMinute': '50',
#                     'saMinute': '50',
#                     'suMinute': '50',
#                     'caloriesYn': 'Y'
#                 }]
#             },
#             'su': {
#                 '1': [],
#                 '2': []
#             },
#             'th': {
#                 '1': [{
#                     'mealIdx': 500022,
#                     'mbrMealIdx': 0,
#                     'name': '던킨도넛 레인보우초코링',
#                     'side': '+사이드, 음료 1종',
#                     'kcal': 523.0,
#                     'carb': 0.0,
#                     'protein': 0.0,
#                     'fat': 0.0,
#                     'salt': 0.0,
#                     'thumbnailUrl': '',
#                     'corner': 'TAKE OUT',
#                     'rating': 0,
#                     'logged': False,
#                     'loggedAll': False,
#                     'mealDt': '20230309',
#                     'status': 1,
#                     'mealCd': '1',
#                     'moHour': '10',
#                     'tuHour': '10',
#                     'weHour': '10',
#                     'thHour': '10',
#                     'frHour': '10',
#                     'saHour': '10',
#                     'suHour': '10',
#                     'moMinute': '50',
#                     'tuMinute': '50',
#                     'weMinute': '50',
#                     'thMinute': '50',
#                     'frMinute': '50',
#                     'saMinute': '50',
#                     'suMinute': '50',
#                     'caloriesYn': 'Y'
#                 }],
#                 '2': [{
#                     'mealIdx': 500006,
#                     'mbrMealIdx': 0,
#                     'name': '닭보쌈구이*파채겉절이',
#                     'side': '쌀밥, 순두부찌개, 비빔막국수, 무말랭이무침, 콘코울슬로, 배추김치',
#                     'kcal': 890.0,
#                     'carb': 0.0,
#                     'protein': 0.0,
#                     'fat': 0.0,
#                     'salt': 0.0,
#                     'thumbnailUrl': '6c50e284-f83a-4a4d-b6c8-029183d3a5b0_28F9386B-B190-4F6B-B1AC-00E05B2CE197.jpeg',
#                     'corner': '백반',
#                     'rating': 0,
#                     'logged': False,
#                     'loggedAll': False,
#                     'mealDt': '20230309',
#                     'status': 1,
#                     'mealCd': '2',
#                     'moHour': '14',
#                     'tuHour': '14',
#                     'weHour': '14',
#                     'thHour': '14',
#                     'frHour': '14',
#                     'saHour': '14',
#                     'suHour': '14',
#                     'moMinute': '50',
#                     'tuMinute': '50',
#                     'weMinute': '50',
#                     'thMinute': '50',
#                     'frMinute': '50',
#                     'saMinute': '50',
#                     'suMinute': '50',
#                     'caloriesYn': 'Y'
#                 }, {
#                     'mealIdx': 500019,
#                     'mbrMealIdx': 0,
#                     'name': '통등심돈까스*만다린샐러드',
#                     'side': '배추김치, 후리가께밥, 우동장국, 분모자매콤떡볶이, 콘코울슬로',
#                     'kcal': 916.0,
#                     'carb': 0.0,
#                     'protein': 0.0,
#                     'fat': 0.0,
#                     'salt': 0.0,
#                     'thumbnailUrl': '318793e1-b373-4428-8909-8ea7ddc0218e_6B3D4A8B-B8EE-4E6C-93EE-17B0E997F1E0.jpeg',
#                     'corner': '스페셜',
#                     'rating': 0,
#                     'logged': False,
#                     'loggedAll': False,
#                     'mealDt': '20230309',
#                     'status': 1,
#                     'mealCd': '2',
#                     'moHour': '14',
#                     'tuHour': '14',
#                     'weHour': '14',
#                     'thHour': '14',
#                     'frHour': '14',
#                     'saHour': '14',
#                     'suHour': '14',
#                     'moMinute': '50',
#                     'tuMinute': '50',
#                     'weMinute': '50',
#                     'thMinute': '50',
#                     'frMinute': '50',
#                     'saMinute': '50',
#                     'suMinute': '50',
#                     'caloriesYn': 'Y'
#                 }, {
#                     'mealIdx': 500013,
#                     'mbrMealIdx': 0,
#                     'name': '청포도리코타치즈 샐러드/크로와상햄치즈 샌드위치',
#                     'side': '+사이드, 음료 1종',
#                     'kcal': 396.0,
#                     'carb': 0.0,
#                     'protein': 0.0,
#                     'fat': 0.0,
#                     'salt': 0.0,
#                     'thumbnailUrl': '54b1e764-8d62-4ea8-ac73-31623fcb7830_0DAACE5A-A373-4542-B747-108AA8C023D3.jpeg',
#                     'corner': 'TAKE OUT',
#                     'rating': 0,
#                     'logged': False,
#                     'loggedAll': False,
#                     'mealDt': '20230309',
#                     'status': 1,
#                     'mealCd': '2',
#                     'moHour': '14',
#                     'tuHour': '14',
#                     'weHour': '14',
#                     'thHour': '14',
#                     'frHour': '14',
#                     'saHour': '14',
#                     'suHour': '14',
#                     'moMinute': '50',
#                     'tuMinute': '50',
#                     'weMinute': '50',
#                     'thMinute': '50',
#                     'frMinute': '50',
#                     'saMinute': '50',
#                     'suMinute': '50',
#                     'caloriesYn': 'Y'
#                 }]
#             },
#             'fr': {
#                 '1': [{
#                     'mealIdx': 500010,
#                     'mbrMealIdx': 0,
#                     'name': '부시맨브레드*이즈니버터',
#                     'side': '+사이드, 음료 1종',
#                     'kcal': 368.0,
#                     'carb': 0.0,
#                     'protein': 0.0,
#                     'fat': 0.0,
#                     'salt': 0.0,
#                     'thumbnailUrl': '',
#                     'corner': 'TAKE OUT',
#                     'rating': 0,
#                     'logged': False,
#                     'loggedAll': False,
#                     'mealDt': '20230310',
#                     'status': 1,
#                     'mealCd': '1',
#                     'moHour': '10',
#                     'tuHour': '10',
#                     'weHour': '10',
#                     'thHour': '10',
#                     'frHour': '10',
#                     'saHour': '10',
#                     'suHour': '10',
#                     'moMinute': '50',
#                     'tuMinute': '50',
#                     'weMinute': '50',
#                     'thMinute': '50',
#                     'frMinute': '50',
#                     'saMinute': '50',
#                     'suMinute': '50',
#                     'caloriesYn': 'Y'
#                 }],
#                 '2': [{
#                     'mealIdx': 500032,
#                     'mbrMealIdx': 0,
#                     'name': '얼큰낙차새전골',
#                     'side': '쌀밥, 비엔나케찹볶음, 단호박부꾸미, 부추무침, 누룽지샐러드, 배추김치',
#                     'kcal': 721.0,
#                     'carb': 0.0,
#                     'protein': 0.0,
#                     'fat': 0.0,
#                     'salt': 0.0,
#                     'thumbnailUrl': 'e1381867-395b-4680-9166-a28b4d23b3fc_834AC877-5CD8-4DED-878C-9A95DE52E9A9.jpeg',
#                     'corner': '백반',
#                     'rating': 0,
#                     'logged': False,
#                     'loggedAll': False,
#                     'mealDt': '20230310',
#                     'status': 1,
#                     'mealCd': '2',
#                     'moHour': '14',
#                     'tuHour': '14',
#                     'weHour': '14',
#                     'thHour': '14',
#                     'frHour': '14',
#                     'saHour': '14',
#                     'suHour': '14',
#                     'moMinute': '50',
#                     'tuMinute': '50',
#                     'weMinute': '50',
#                     'thMinute': '50',
#                     'frMinute': '50',
#                     'saMinute': '50',
#                     'suMinute': '50',
#                     'caloriesYn': 'Y'
#                 }, {
#                     'mealIdx': 500034,
#                     'mbrMealIdx': 0,
#                     'name': '중화짜장밥*계란후라이',
#                     'side': '게살스프, 찹쌀꿔바로우, 단무지, 누룽지샐러드, 배추김치',
#                     'kcal': 750.0,
#                     'carb': 0.0,
#                     'protein': 0.0,
#                     'fat': 0.0,
#                     'salt': 0.0,
#                     'thumbnailUrl': 'dc2913c9-a019-46cb-a0ce-f55199ee9867_35DFC729-59FF-489C-B5C4-0AE8EFE37CB2.jpeg',
#                     'corner': '스페셜',
#                     'rating': 0,
#                     'logged': False,
#                     'loggedAll': False,
#                     'mealDt': '20230310',
#                     'status': 1,
#                     'mealCd': '2',
#                     'moHour': '14',
#                     'tuHour': '14',
#                     'weHour': '14',
#                     'thHour': '14',
#                     'frHour': '14',
#                     'saHour': '14',
#                     'suHour': '14',
#                     'moMinute': '50',
#                     'tuMinute': '50',
#                     'weMinute': '50',
#                     'thMinute': '50',
#                     'frMinute': '50',
#                     'saMinute': '50',
#                     'suMinute': '50',
#                     'caloriesYn': 'Y'
#                 }, {
#                     'mealIdx': 500018,
#                     'mbrMealIdx': 0,
#                     'name': '프로틴업 샐러드/키토소시지 김밥',
#                     'side': '+사이드, 음료 1종',
#                     'kcal': 386.0,
#                     'carb': 0.0,
#                     'protein': 0.0,
#                     'fat': 0.0,
#                     'salt': 0.0,
#                     'thumbnailUrl': '1a5b07ae-540d-4e3c-8513-257186f89d06_5069200D-898A-4ACB-9CB7-87E5E1551A2B.jpeg',
#                     'corner': 'TAKE OUT',
#                     'rating': 0,
#                     'logged': False,
#                     'loggedAll': False,
#                     'mealDt': '20230310',
#                     'status': 1,
#                     'mealCd': '2',
#                     'moHour': '14',
#                     'tuHour': '14',
#                     'weHour': '14',
#                     'thHour': '14',
#                     'frHour': '14',
#                     'saHour': '14',
#                     'suHour': '14',
#                     'moMinute': '50',
#                     'tuMinute': '50',
#                     'weMinute': '50',
#                     'thMinute': '50',
#                     'frMinute': '50',
#                     'saMinute': '50',
#                     'suMinute': '50',
#                     'caloriesYn': 'Y'
#                 }]
#             },
#             'we': {
#                 '1': [{
#                     'mealIdx': 500025,
#                     'mbrMealIdx': 0,
#                     'name': '아이돌샌드위치',
#                     'side': '+사이드, 음료 1종',
#                     'kcal': 726.0,
#                     'carb': 0.0,
#                     'protein': 0.0,
#                     'fat': 0.0,
#                     'salt': 0.0,
#                     'thumbnailUrl': '',
#                     'corner': 'TAKE OUT',
#                     'rating': 0,
#                     'logged': False,
#                     'loggedAll': False,
#                     'mealDt': '20230308',
#                     'status': 2,
#                     'mealCd': '1',
#                     'moHour': '10',
#                     'tuHour': '10',
#                     'weHour': '10',
#                     'thHour': '10',
#                     'frHour': '10',
#                     'saHour': '10',
#                     'suHour': '10',
#                     'moMinute': '50',
#                     'tuMinute': '50',
#                     'weMinute': '50',
#                     'thMinute': '50',
#                     'frMinute': '50',
#                     'saMinute': '50',
#                     'suMinute': '50',
#                     'caloriesYn': 'Y'
#                 }],
#                 '2': [{
#                     'mealIdx': 500007,
#                     'mbrMealIdx': 0,
#                     'name': '직화쭈꾸미불고기*콩나물찜',
#                     'side': '쌀밥, 소고기미역국, 카레고로케, 깻잎*쌈무*날치알마요, 양배추샐러드, 배추김치',
#                     'kcal': 886.0,
#                     'carb': 0.0,
#                     'protein': 0.0,
#                     'fat': 0.0,
#                     'salt': 0.0,
#                     'thumbnailUrl': 'c322bf95-5558-420b-97f7-0eec78cd6294_CCC7C1D9-4059-4E16-8AF4-2C83E9486012.jpeg',
#                     'corner': '백반',
#                     'rating': 0,
#                     'logged': False,
#                     'loggedAll': False,
#                     'mealDt': '20230308',
#                     'status': 1,
#                     'mealCd': '2',
#                     'moHour': '14',
#                     'tuHour': '14',
#                     'weHour': '14',
#                     'thHour': '14',
#                     'frHour': '14',
#                     'saHour': '14',
#                     'suHour': '14',
#                     'moMinute': '50',
#                     'tuMinute': '50',
#                     'weMinute': '50',
#                     'thMinute': '50',
#                     'frMinute': '50',
#                     'saMinute': '50',
#                     'suMinute': '50',
#                     'caloriesYn': 'Y'
#                 }, {
#                     'mealIdx': 500020,
#                     'mbrMealIdx': 0,
#                     'name': '텐동',
#                     'side': '유부미소시루, 토마토유자절임, 락교&초생강, 양배추샐러드, 배추김치',
#                     'kcal': 785.0,
#                     'carb': 0.0,
#                     'protein': 0.0,
#                     'fat': 0.0,
#                     'salt': 0.0,
#                     'thumbnailUrl': '7b757bcf-3acf-4c61-a3fe-527d5fde85a2_D85CA9F7-0A86-4242-B5D7-598CD4A4027D.jpeg',
#                     'corner': '스페셜',
#                     'rating': 0,
#                     'logged': False,
#                     'loggedAll': False,
#                     'mealDt': '20230308',
#                     'status': 1,
#                     'mealCd': '2',
#                     'moHour': '14',
#                     'tuHour': '14',
#                     'weHour': '14',
#                     'thHour': '14',
#                     'frHour': '14',
#                     'saHour': '14',
#                     'suHour': '14',
#                     'moMinute': '50',
#                     'tuMinute': '50',
#                     'weMinute': '50',
#                     'thMinute': '50',
#                     'frMinute': '50',
#                     'saMinute': '50',
#                     'suMinute': '50',
#                     'caloriesYn': 'Y'
#                 }, {
#                     'mealIdx': 500033,
#                     'mbrMealIdx': 0,
#                     'name': '케이준치킨 샐러드/스팸김치 컵밥',
#                     'side': '+사이드, 음료 1종',
#                     'kcal': 561.0,
#                     'carb': 0.0,
#                     'protein': 0.0,
#                     'fat': 0.0,
#                     'salt': 0.0,
#                     'thumbnailUrl': 'f82ded24-767b-48c8-b059-05fcd03b4156_E789B820-7FAB-4F34-935F-72533B28E8F8.jpeg',
#                     'corner': 'TAKE OUT',
#                     'rating': 0,
#                     'logged': False,
#                     'loggedAll': False,
#                     'mealDt': '20230308',
#                     'status': 2,
#                     'mealCd': '2',
#                     'moHour': '14',
#                     'tuHour': '14',
#                     'weHour': '14',
#                     'thHour': '14',
#                     'frHour': '14',
#                     'saHour': '14',
#                     'suHour': '14',
#                     'moMinute': '50',
#                     'tuMinute': '50',
#                     'weMinute': '50',
#                     'thMinute': '50',
#                     'frMinute': '50',
#                     'saMinute': '50',
#                     'suMinute': '50',
#                     'caloriesYn': 'Y'
#                 }]
#             },
#             'sa': {
#                 '1': [],
#                 '2': []
#             }
#         }
#     }
#     mocked_get.text = json.dumps(sample_response)
