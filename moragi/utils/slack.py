import datetime
from http import HTTPStatus

import pytz
from slack_sdk.webhook import WebhookClient
from slack_sdk.webhook.webhook_response import WebhookResponse

from moragi.models.cj_fresh_meal_response_model import Meal
from moragi.utils import console


def send_slack_message(url: str, breakfast_options: list[Meal], lunch_options: list[Meal]):
    webhook = WebhookClient(url)
    console.log('Sending message to Slack')
    response: WebhookResponse = webhook.send(
        text='모락이에요!',
        blocks=_make_slack_blocks(breakfast_options, lunch_options),
    )
    console.log('Sent Message to slack with response', _webhook_response_to_dict(response))

    assert response.status_code == HTTPStatus.OK.value


def _make_slack_blocks(breakfast_options: list[Meal], lunch_options: list[Meal]):

    return [{
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': f'안녕하세요! 모락이에요. 🙇‍♂️ 오늘은 {_get_date_string()}이에요!'
        },
    }, {
        'type': 'divider'
    }, {
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': '먼저 아침 메뉴부터 알려드릴게요! 🥪'
        },
    }] + _get_options_block(breakfast_options) + [{
        'type': 'divider'
    }, {
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': '그리고 점심 메뉴를 알려드릴게요! 🍚'
        },
    }] + _get_options_block(lunch_options) + [{
        'type': 'divider'
    }, {
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': '오늘 하루도 행복한 하루 되세요! 🥰 모락이는 또 돌아오겠습니다! 🙌'
        }
    }]


def _get_date_string():
    date = datetime.datetime.utcnow().astimezone(pytz.timezone('Asia/Seoul'))
    month: int = date.month
    day: int = date.day
    return f'{month}월 {day}일'


def _get_options_block(options: list[Meal]) -> list[dict[str, str]]:
    blocks = []
    for option in options:
        blocks.append({
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': f'''
*{option.corner}*
- {option.name}
- {option.side}
- _{option.kcal} 칼로리_
'''[1:]
            }
        })
        if option.thumbnail_url:
            blocks.append({'type': 'section', 'text': {'type': 'mrkdwn', 'text': '음식 사진도 들고왔어요! 📸 👇👇👇'}})
            blocks.append({'type': 'image', 'image_url': option.thumbnail_url, 'alt_text': option.name})
        blocks.append({
            'type': 'actions',
            'elements': [{
                'type': 'button',
                'text': {
                    'type': 'plain_text',
                    'text': '자세히 보러가기'
                },
                'action_id': 'button',
                'url': f'https://front.cjfreshmeal.co.kr/menu/detail/{option.meal_index}',
            }]
        })
    return blocks


def _webhook_response_to_dict(instance: WebhookResponse):
    return {
        'api_url': instance.api_url,
        'status_code': instance.status_code,
        'body': instance.body,
        'headers': instance.headers,
    }
