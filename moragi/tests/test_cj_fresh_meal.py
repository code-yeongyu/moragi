import json
from unittest.mock import MagicMock, Mock, patch

import pytest

from moragi.utils.cj_fresh_meal import CJFreshMealClient


class TestCJFreshMealClient:

    @pytest.fixture
    def cj_fresh_meal_client(self):
        return CJFreshMealClient(store_id=1)

    @patch('httpx.Client.get')
    def test_fail__when_get_today_meal_no_data(
        self,
        mock_get: MagicMock,
        cj_fresh_meal_client: CJFreshMealClient,
    ):
        # given
        no_data_response = {
            'status': 'success',
            'retCode': '00',
            'retMsg': '',
            'date': 'Sun Mar 12 03:45:51 KST 2023',
            'data': {}
        }
        mock_get.return_value = Mock(text=json.dumps(no_data_response))

        # when
        daily_menu = cj_fresh_meal_client.get_today_meal()

        # then
        assert daily_menu is None
