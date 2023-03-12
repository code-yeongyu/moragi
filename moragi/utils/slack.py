import datetime
import random
from http import HTTPStatus

import pytz
from slack_sdk.webhook import WebhookClient
from slack_sdk.webhook.webhook_response import WebhookResponse

from moragi.models.menu import DailyMenu, Menu
from moragi.utils import console


class MealSummarySender:

    def __init__(self, url: str, daily_menu: DailyMenu):
        self.url = url
        self.daily_menu = daily_menu

    def run(self):
        webhook = WebhookClient(self.url)
        console.log('Sending message to Slack')
        response: WebhookResponse = webhook.send(
            text='모락이에요!',
            blocks=self._get_slack_blocks(),
        )
        console.log('Sent Message to slack with response', _webhook_response_to_dict(response))
        assert response.status_code == HTTPStatus.OK.value

    def _get_slack_blocks(self):
        blocks = [{
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': f'안녕하세요! 모락이에요. 🙇‍♂️ 오늘은 {self._get_date_string()}이에요!'
            },
        }, {
            'type': 'divider'
        }]

        if self.daily_menu.breakfast:
            blocks.extend([{
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '먼저 아침 메뉴부터 알려드릴게요! 🥪'
                },
            }] + self._get_options_block(self.daily_menu.breakfast) + [{
                'type': 'divider'
            }])

        if self.daily_menu.lunch:
            blocks.extend([{
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '그리고 점심 메뉴를 알려드릴게요! 🍚'
                },
            }] + self._get_options_block(self.daily_menu.lunch) + [{
                'type': 'divider'
            }])

        if self.daily_menu.dinner:
            blocks.extend([{
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '저녁 메뉴는 다음과 같아요! 🍽️'
                }
            }] + self._get_options_block(self.daily_menu.lunch) + [{
                'type': 'divider'
            }])

        blocks.append({
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': '오늘 하루도 행복한 하루 되세요! 🥰 모락이는 또 돌아오겠습니다! 🙌'
            }
        })
        return blocks

    def _get_date_string(self):
        date = datetime.datetime.utcnow().astimezone(pytz.timezone('Asia/Seoul'))
        month: int = date.month
        day: int = date.day
        return f'{month}월 {day}일'

    def _get_options_block(self, options: list[Menu]) -> list[dict[str, str]]:
        blocks = []
        for option in options:
            blocks.append({
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f'''
*{option.food_type}*
• {option.name}
• {option.side}
_{option.kcal} 칼로리_
'''[1:]
                }
            })
        return blocks


class LunchWithPhotoSender:
    '''CJ 프레시밀에 점심 이미지가 약 오전 11시 20분 이후에 업로드 되므로, 해당 시간 이후를 위한 클래스'''

    def __init__(self, url: str, lunch_options: list[Menu]):
        self.url = url
        self.lunch_options = lunch_options

    def run(self):
        webhook = WebhookClient(self.url)
        console.log('Sending message to Slack')
        response: WebhookResponse = webhook.send(
            text='모락이에요!',
            blocks=self._get_slack_blocks(),
        )
        console.log('Sent Message to slack with response', _webhook_response_to_dict(response))
        assert response.status_code == HTTPStatus.OK.value

    def _get_slack_blocks(self):
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

        blocks = [{
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': f'{random.choice(greetings_start)} {random.choice(greetings_end)}'
            },
        }, {
            'type': 'divider'
        }] + self._get_options_block(self.lunch_options) + [{
            'type': 'divider'
        }, {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': random.choice(closes)
            }
        }]

        return blocks

    def _get_options_block(self, options: list[Menu]) -> list[dict[str, str]]:
        blocks = []
        for option in options:
            blocks.extend([{
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f'''
*{option.food_type}*
• {option.name}
'''[1:]
                }
            }, {
                'type': 'image',
                'image_url': option.thumbnail_url,
                'alt_text': option.name
            }, {
                'type': 'actions',
                'elements': [{
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': '자세히 보러가기',
                        'action_id': 'button',
                        'url': option.detail_info_url
                    }
                }]
            }])
        return blocks


def _webhook_response_to_dict(instance: WebhookResponse):
    return {
        'api_url': instance.api_url,
        'status_code': instance.status_code,
        'body': instance.body,
    }
