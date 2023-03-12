from typing import Any

from moragi.models.menu import DailyMenu, Menu, WeeklyMenu

SLACK_BLOCK_TYPE = list[dict[str, Any]]


def simple_menu_block(menu: Menu):
    return {
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': f'''
*{menu.food_type}*
• {menu.name}
• {menu.side}
_{menu.kcal} 칼로리_
'''[1:]
        }
    }


def image_menu_block(menu: Menu):
    return [{
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': f'''
*{menu.food_type}*
• {menu.name}
'''[1:]
        }
    }, {
        'type': 'image',
        'image_url': menu.thumbnail_url,
        'alt_text': menu.name
    }, {
        'type': 'actions',
        'elements': [{
            'type': 'button',
            'text': {
                'type': 'plain_text',
                'text': '자세히 보러가기',
                'action_id': 'button',
                'url': menu.detail_info_url
            }
        }]
    }]


def simple_menu_list_block(menu_list: list[Menu]):
    return [{
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': f'''
*{menu.food_type}*
• {menu.name}
• {menu.side}
_{menu.kcal} 칼로리_
'''[1:]
        }
    } for menu in menu_list]


def image_menu_list_block(menu_list: list[Menu]):
    return [block for menu in menu_list for block in image_menu_block(menu)]


def daily_menu_list_block(daily_menu: DailyMenu) -> SLACK_BLOCK_TYPE:
    blocks = []
    if daily_menu.breakfast:
        blocks += [{
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': '먼저 아침 메뉴부터 알려드릴게요! 🥪'
            },
        }] + simple_menu_list_block(daily_menu.breakfast) + [{
            'type': 'divider'
        }]

    if daily_menu.lunch:
        blocks += ([{
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': '그리고 점심 메뉴를 알려드릴게요! 🍚'
            },
        }] + simple_menu_list_block(daily_menu.lunch) + [{
            'type': 'divider'
        }])

    if daily_menu.dinner:
        blocks += [{
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': '저녁 메뉴는 다음과 같아요! 🍽️'
            }
        }] + simple_menu_list_block(daily_menu.lunch) + [{
            'type': 'divider'
        }]

    return blocks


def weekly_menu_list_block(menu_list: WeeklyMenu) -> SLACK_BLOCK_TYPE:
    blocks = []

    if menu_list.monday:
        blocks += [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '월요일 메뉴는 다음과 같아요! 🍽️'
                }
            },
            *daily_menu_list_block(menu_list.monday),
        ]

    if menu_list.tuesday:
        blocks += [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '화요일 메뉴는 다음과 같아요! 🍽️'
                }
            },
            *daily_menu_list_block(menu_list.tuesday),
        ]

    if menu_list.wednesday:
        blocks += [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '수요일 메뉴는 다음과 같아요! 🍽️'
                }
            },
            *daily_menu_list_block(menu_list.wednesday),
        ]

    if menu_list.thursday:
        blocks += [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '목요일 메뉴는 다음과 같아요! 🍽️'
                }
            },
            *daily_menu_list_block(menu_list.thursday),
        ]

    if menu_list.friday:
        blocks += [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '금요일 메뉴는 다음과 같아요! 🍽️'
                }
            },
            *daily_menu_list_block(menu_list.friday),
        ]

    if menu_list.saturday:
        blocks += [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '토요일 메뉴는 다음과 같아요! 🍽️'
                }
            },
            *daily_menu_list_block(menu_list.saturday),
        ]

    if menu_list.sunday:
        blocks += [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '일요일 메뉴는 다음과 같아요! 🍽️'
                }
            },
            *daily_menu_list_block(menu_list.sunday),
        ]

    return blocks
