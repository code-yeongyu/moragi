import datetime
import random
from abc import ABC, abstractmethod
from typing import Any

import pytz

from moragi.models.menu import DailyMenu, Menu, WeeklyMenu
from moragi.utils.slack.blocks import (
    daily_menu_list_block,
    image_menu_list_block,
    weekly_menu_list_block,
)


class SlackMessageBuilder(ABC):

    @abstractmethod
    def make_slack_blocks(self) -> list[dict[str, Any]]:
        pass


class MenuSummaryMessageBuilder(SlackMessageBuilder):

    def __init__(self, daily_menu: DailyMenu):
        self.daily_menu = daily_menu

    def make_slack_blocks(self):
        return [{
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': f'안녕하세요! 모락이에요. 🙇‍♂️ 오늘은 {self._get_date_string()}이에요!'
            },
        }, {
            'type': 'divider'
        }, *daily_menu_list_block(self.daily_menu), {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': '오늘 하루도 행복한 하루 되세요! 🥰 모락이는 또 돌아오겠습니다! 🙌'
            }
        }]

    def _get_date_string(self):
        date = datetime.datetime.utcnow().astimezone(pytz.timezone('Asia/Seoul'))
        month: int = date.month
        day: int = date.day
        return f'{month}월 {day}일'


class LunchWithPhotoMessageBuilder(SlackMessageBuilder):
    '''CJ 프레시밀에 점심 이미지가 약 오전 11시 20분 이후에 업로드 되므로, 해당 시간 이후를 위한 클래스'''

    def __init__(self, lunch_menu_list: list[Menu]):
        self.lunch_menu_list = lunch_menu_list

    def make_slack_blocks(self):
        greetings_start = [
            '안녕하세요! 모락이에요 🙇‍♂️',
            '안녕하세요! 신입사원 모락이에요 🐥 ',
            '안녕하세요! 모락이입니다 🙋‍♂️',
            '반갑습니다! 모락이에요 🙋‍♂️',
        ]
        greetings_end = [
            '점심 메뉴가 준비된거같아 살짝 가서 찍어왔어요 📸',
            '오늘도 몰래가서 슬쩍 📸',
            '배고프시죠?! 그럴줄 알고 점심 메뉴를 찍어왔답니다 📸',
        ]
        closes = [
            '식사 맛있게 하세요 😋',
            '저는 이만 가볼게요! 🙋‍♂️',
            '모락이는 또 돌아오겠습니다! 🙌',
            '으악 나도 먹고싶다 😋',
            '저는 로봇일텐데 왜 사진보니까 배가 고플까요 🤔',
            '우와 오늘 진짜 맛있어보여요 🍚',
        ]

        return [{
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': f'{random.choice(greetings_start)} {random.choice(greetings_end)}'
            },
        }, {
            'type': 'divider'
        }, *image_menu_list_block(self.lunch_menu_list), {
            'type': 'divider'
        }, {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': random.choice(closes)
            }
        }]

        return blocks
