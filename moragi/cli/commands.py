from typer import Typer

from moragi.cli.meal_utils import get_today_lunch_with_image, get_today_meal
from moragi.utils.slack import LunchWithPhotoMessageBuilder, MealSummaryMessageBuilder, SlackMessageSender

cli_app = Typer()


@cli_app.command()
def send_daily_meal_summary(cj_fresh_meal_store_id: int, slack_webhook_url: str):
    daily_menu = get_today_meal(cj_fresh_meal_store_id)
    builder = MealSummaryMessageBuilder(daily_menu)
    sender = SlackMessageSender(slack_webhook_url, builder)
    sender.run()


@cli_app.command()
def send_daily_meal_summary_with_photo(cj_fresh_meal_store_id: int, slack_webhook_url: str):
    lunch_options = get_today_lunch_with_image(cj_fresh_meal_store_id)
    builder = LunchWithPhotoMessageBuilder(lunch_options)
    sender = SlackMessageSender(slack_webhook_url, builder)
    sender.run()


# todo: implement next meal (tommorow or next week monday)
