from moragi.models.menu import Menu


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
    return [block for option in menu_list for block in image_menu_block(option)]
