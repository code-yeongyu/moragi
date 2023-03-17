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

    today_weekday = datetime.datetime.utcnow().astimezone(pytz.timezone('Asia/Seoul')).weekday()
    is_today_friday = today_weekday == Weekday.FRIDAY
    if is_today_friday:
        weekly_menu = client.get_week_meal(WeekType.NEXT_WEEK)
        if not weekly_menu.monday:
            raise Exception("Error while getting next week's monday's menu")
        builder = FridayAfternoonMessageBuilder(weekly_menu.monday)
    else:
        weekly_menu = client.get_week_meal(WeekType.THIS_WEEK)
        tommorow_menu: Optional[DailyMenu] = None
        if today_weekday == Weekday.MONDAY:
            tommorow_menu = weekly_menu.tuesday
        elif today_weekday == Weekday.TUESDAY:
            tommorow_menu = weekly_menu.wednesday
        elif today_weekday == Weekday.WEDNESDAY:
            tommorow_menu = weekly_menu.thursday
        elif today_weekday == Weekday.THURSDAY:
            tommorow_menu = weekly_menu.friday
        else:
            raise Exception('Today is not supported day')

        if not tommorow_menu:
            raise Exception("Error while getting tommorow's menu")
        builder = TommorowMenuMessageBuilder(tommorow_menu)

    sender = SlackMessageSender(slack_webhook_url, builder)
    sender.run()
