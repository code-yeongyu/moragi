from typing import Any

from moragi.models.menu import DailyMenu, Menu

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
        'image_url': menu.resized_thumbnail_url,
        'alt_text': menu.name
    }, {
        'type': 'actions',
        'elements': [{
            'type': 'button',
            'action_id': 'button',
            'text': {
                'type': 'plain_text',
                'text': '자세히 보러가기',
            },
            'url': menu.detail_info_url
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


def section_menu_list_block(menu_list: list[Menu]):

    def _side_to_string(side: str) -> str:
        items = side.split(', ')
        formatted_items = [f'• {item}' for item in items]
        formatted_string = '\n'.join(formatted_items)
        return formatted_string

    return [{
        'type': 'section',
        'fields': [{
            'type': 'mrkdwn',
            'text': f'''
*{menu.food_type}*
• {menu.name}
{_side_to_string(menu.side)}
_{menu.kcal} 칼로리_
'''[1:],
        } for menu in menu_list]
    }]


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
        }] + simple_menu_list_block(daily_menu.dinner) + [{
            'type': 'divider'
        }]

    return blocks
