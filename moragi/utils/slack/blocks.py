from typing import Any, Optional

from moragi.models.menu import DailyMenu, Menu

SLACK_BLOCK_TYPE = list[dict[str, Any]]


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


def image_menu_list_block(menu_list: list[Menu]):
    return [block for menu in menu_list for block in image_menu_block(menu)]


def section_menu_list_block(menu_list: list[Menu]):

    def _side_to_string(side: Optional[str]) -> str:
        if not side:
            return ''
        items = side.split(', ')
        formatted_items = [f'• {item}' for item in items]
        formatted_string = '\n'.join(formatted_items)
        return formatted_string

    return [{
        'type': 'section',
        'fields': [{
            'type': 'mrkdwn',
            'text': f'''
*{menu.food_type}* _{menu.kcal} 칼로리_
• {menu.name}
{_side_to_string(menu.side)}
'''[1:],
        } for menu in menu_list]
    }]


def daily_menu_list_block(daily_menu: DailyMenu) -> SLACK_BLOCK_TYPE:
    blocks = []
    if daily_menu.breakfast:
        blocks += [{
            'type': 'header',
            'text': {
                'type': 'plain_text',
                'text': '먼저 아침 메뉴입니다! 🥪'
            },
        }] + section_menu_list_block(daily_menu.breakfast) + [{
            'type': 'divider'
        }]

    if daily_menu.lunch:
        blocks += ([{
            'type': 'header',
            'text': {
                'type': 'plain_text',
                'text': '점심 메뉴를 알려드릴게요! 🍚'
            },
        }] + section_menu_list_block(daily_menu.lunch) + [{
            'type': 'divider'
        }])

    if daily_menu.dinner:
        blocks += [{
            'type': 'header',
            'text': {
                'type': 'plain_text',
                'text': '저녁 메뉴는 다음과 같아요! 🍽️'
            }
        }] + section_menu_list_block(daily_menu.dinner) + [{
            'type': 'divider'
        }]

    return blocks
