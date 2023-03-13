import datetime
from typing import Optional

import pytz
from typer import Typer

from moragi.cli.cj_fresh_meal_utils import get_today_lunch_with_image
from moragi.models import Weekday
from moragi.models.cj_fresh_meal import WeekType
from moragi.models.menu import DailyMenu
from moragi.utils.cj_fresh_meal import CJFreshMealClient
from moragi.utils.slack import (
    FridayAfternoonMessageBuilder,
    LunchWithPhotoMessageBuilder,
    SlackMessageBuilder,
    SlackMessageSender,
    TommorowMenuMessageBuilder,
)

cli_app = Typer()


@cli_app.command()
def send_daily_menu_summary_with_photo(cj_fresh_meal_store_id: int, slack_webhook_url: str):
    # https://console.cron-job.org/jobs/4229777 (29 11 * * 1-5)
    lunch_options = get_today_lunch_with_image(cj_fresh_meal_store_id)
    builder = LunchWithPhotoMessageBuilder(lunch_options)
    sender = SlackMessageSender(slack_webhook_url, builder)
    sender.run()


@cli_app.command()
def send_next_menu_summary(cj_fresh_meal_store_id: int, slack_webhook_url: str):
    # https://console.cron-job.org/jobs/4233822 (59 17 * * 1-5)
    client = CJFreshMealClient(cj_fresh_meal_store_id)
    builder: SlackMessageBuilder

    is_today_friday = \
        datetime.datetime.utcnow().astimezone(pytz.timezone('Asia/Seoul')).weekday() == Weekday.FRIDAY
    if is_today_friday:
        week_menu = client.get_week_meal(WeekType.NEXT_WEEK)
        if not week_menu:
            raise Exception("Error while getting next week's menu")
        if not week_menu.monday:
            raise Exception("Error while getting next week's monday's menu")
        builder = FridayAfternoonMessageBuilder(week_menu.monday)
    else:
        week_menu = client.get_week_meal(WeekType.THIS_WEEK)
        if not week_menu:
            raise Exception('Error while getting next week menu')

        weekday = Weekday(datetime.date.today().weekday())
        tommorow_menu: Optional[DailyMenu] = None
        if weekday == Weekday.MONDAY:
            tommorow_menu = week_menu.tuesday
        elif weekday == Weekday.TUESDAY:
            tommorow_menu = week_menu.wednesday
        elif weekday == Weekday.WEDNESDAY:
            tommorow_menu = week_menu.thursday
        elif weekday == Weekday.THURSDAY:
            tommorow_menu = week_menu.friday

        if not tommorow_menu:
            raise Exception("Error while getting tommorow's menu")
        builder = TommorowMenuMessageBuilder(tommorow_menu)

    sender = SlackMessageSender(slack_webhook_url, builder)
    sender.run()
