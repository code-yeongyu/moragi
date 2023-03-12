import datetime
import random
from abc import ABC, abstractmethod
from typing import Any

import pytz

from moragi.models import Weekday
from moragi.models.menu import DailyMenu, Menu
from moragi.utils.slack.blocks import (
    daily_menu_list_block,
    image_menu_list_block,
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


class TommorowMenuMessageBuilder(SlackMessageBuilder):

    def __init__(self, tommorow_menu: DailyMenu):
        self.daily_menu = tommorow_menu

    def make_slack_blocks(self):
        greetings_start = [
            '안녕하세요! 모락이에요 🙇‍♂️',
            '안녕하세요! 신입사원 모락이에요 🐥 ',
            '안녕하세요! 모락이입니다 🙋‍♂️',
            '모락이에요! 🙋‍♂️',
            '모락이가 왔습니다! 🙋‍♂️',
        ]
        greetings_end = [
            '\n내일의 메뉴가 도착했어요! 🍙',
            '\n내일의 메뉴를 들고 왔답니다! 🍚',
            '\n내일 나오는 메뉴가 궁금해서 그새 또 다녀왔어요! 🍽️',
        ]
        closings = [
            '오늘 하루도 행복한 하루 되세요! 🥰',
            '저는 이만 가볼게요! 🙋‍♂️',
            '모락이는 또 돌아오겠습니다! 🙌',
            '업무에 참고 하시길 바랍니다 📁',
            '오늘 하루도 수고 많으셨습니다! 🙇‍♂️',
        ]
        return [{
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': \
                    f'{random.choice(greetings_start)} \
내일은 {self._get_tommorow_date_string()}인데요! {random.choice(greetings_end)}'
            },
        }, {
            'type': 'divider'
        }, *daily_menu_list_block(self.daily_menu), {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': random.choice(closings)
            },
        }]

    def _get_tommorow_date_string(self):
        date = datetime.datetime.utcnow().astimezone(pytz.timezone('Asia/Seoul'))
        date += datetime.timedelta(days=1)
        month: int = date.month
        day: int = date.day
        return f'{month}월 {day}일'


class FridayAfternoonMessageBuilder(SlackMessageBuilder):

    def __init__(self, monday_menu: DailyMenu):
        self.monday_menu = monday_menu

    def make_slack_blocks(self):
        greetings_start = [
            '안녕하세요! 모락이에요 🙇‍♂️',
            '안녕하세요! 신입사원 모락이에요 🐥 ',
            '안녕하세요! 모락이입니다 🙋‍♂️',
            '모락이에요! 🙋‍♂️',
            '모락이가 왔습니다! 🙋‍♂️',
        ]
        greetings_end = [
            '벌써 금요일이에요! 🙌\n다음주 월요일 메뉴를 알려드릴게요! 🍙',
            '벌써 금요일입니다! 🙌\n다음주 월요일 메뉴를 들고 왔어요! 🍚',
            '이제 금요일 오후 입니다! 🙌\n다음주 월요일 메뉴가 궁금해서 그새 또 다녀왔어요! 🍽️',
        ]
        closings = [
            '좋은 주말 되세요! 모락이는 월요일 점심에 다시 찾아오겠습니다 🙇‍♂️',
            '주말 잘 보내세요! 모락이는 월요일 점심에 다시 찾아오겠습니다 🙇‍♂️',
            '주말에 푹 쉬고 월요일에 뵈어요! 🙌',
        ]
        return [{
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': \
                    f'{random.choice(greetings_start)} {random.choice(greetings_end)} \
 다음주 월요일은 {self._get_monday_date_string()}이에요!'
            },
        }, {
            'type': 'divider'
        }, *daily_menu_list_block(self.monday_menu), {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': random.choice(closings)
            },
        }]

    def _get_monday_date_string(self):
        date = datetime.datetime.utcnow().astimezone(pytz.timezone('Asia/Seoul'))
        while Weekday(date.weekday()) != Weekday.MONDAY:
            date += datetime.timedelta(days=1)
        month: int = date.month
        day: int = date.day
        return f'{month}월 {day}일'
