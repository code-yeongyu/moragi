import datetime
from typing import Optional

import pytz
from typer import Typer

from moragi.cli.cj_fresh_meal_utils import get_menu_with_image, get_today_meal
from moragi.models import Weekday
from moragi.models.cj_fresh_meal import WeekType
from moragi.models.menu import DailyMenu
from moragi.utils.cj_fresh_meal import CJFreshMealClient
from moragi.utils.slack import (
    FridayAfternoonMessageBuilder,
    MenuSummaryMessageBuilder,
    MenuWithPhotoMessageBuilder,
    SlackMessageBuilder,
    SlackMessageSender,
    TextMessageBuilder,
    TomorrowMenuMessageBuilder,
)

cli_app = Typer()


@cli_app.command()
def send_daily_menu_summary_with_photo(cj_fresh_meal_store_id: int, slack_webhook_url: str, is_lunch: bool):
    lunch_options = get_menu_with_image(cj_fresh_meal_store_id, is_lunch=is_lunch)
    builder = MenuWithPhotoMessageBuilder(lunch_options)
    sender = SlackMessageSender(slack_webhook_url, builder)
    sender.run()


@cli_app.command()
def send_lunch_menu_summary_with_photo(cj_fresh_meal_store_id: int, slack_webhook_url: str):
    # alias of send_daily_menu_summary_with_photo
    # https://console.cron-job.org/jobs/4229777 (20 11 * * 1-5)
    send_daily_menu_summary_with_photo(cj_fresh_meal_store_id, slack_webhook_url, is_lunch=True)


@cli_app.command()
def send_dinner_menu_summary_with_photo(cj_fresh_meal_store_id: int, slack_webhook_url: str):
    # alias of send_daily_menu_summary_with_photo
    # https://console.cron-job.org/jobs/4233822 (50 17 * * 1-5)
    send_daily_menu_summary_with_photo(cj_fresh_meal_store_id, slack_webhook_url, is_lunch=False)


@cli_app.command()
def send_next_menu_summary(cj_fresh_meal_store_id: int, slack_webhook_url: str):
    # https://console.cron-job.org/jobs/4262920 (30 18 * * 1-5)
    client = CJFreshMealClient(cj_fresh_meal_store_id)
    builder: SlackMessageBuilder

    today_weekday = \
        Weekday(datetime.datetime.now(pytz.timezone('Asia/Seoul')).weekday())
    is_today_friday = today_weekday == Weekday.FRIDAY
    if is_today_friday:
        weekly_menu = client.get_week_meal(WeekType.NEXT_WEEK)
        if not weekly_menu.monday:
            raise Exception("Error while getting next week's monday's menu")
        builder = FridayAfternoonMessageBuilder(weekly_menu.monday)
    else:
        weekly_menu = client.get_week_meal(WeekType.THIS_WEEK)
        tomorrow_menu: Optional[DailyMenu] = None
        if today_weekday == Weekday.MONDAY:
            tomorrow_menu = weekly_menu.tuesday
        elif today_weekday == Weekday.TUESDAY:
            tomorrow_menu = weekly_menu.wednesday
        elif today_weekday == Weekday.WEDNESDAY:
            tomorrow_menu = weekly_menu.thursday
        elif today_weekday == Weekday.THURSDAY:
            tomorrow_menu = weekly_menu.friday
        else:
            raise Exception('Today is not supported day')

        if not tomorrow_menu:
            raise Exception("Error while getting tommorow's menu")
        builder = TomorrowMenuMessageBuilder(tomorrow_menu)

    sender = SlackMessageSender(slack_webhook_url, builder)
    sender.run()


@cli_app.command()
def send_today_menu_summary(cj_fresh_meal_store_id: int, slack_webhook_url: str):
    # https://console.cron-job.org/jobs/4251142 (0 8 * * 1)
    # just in case if the menu is not uploaded on Friday, send the menu on Monday morning
    daily_menu = get_today_meal(cj_fresh_meal_store_id)

    builder = MenuSummaryMessageBuilder(daily_menu)
    sender = SlackMessageSender(slack_webhook_url, builder)
    sender.run()


@cli_app.command()
def send_message(message: str, slack_webhook_url: str):
    # to manually send a message
    builder = TextMessageBuilder(message)
    sender = SlackMessageSender(slack_webhook_url, builder)
    sender.run()
