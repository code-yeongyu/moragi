from typer import Typer

from moragi.cli.meal_utils import get_today_lunch_with_image, get_today_meal
from moragi.utils import slack

cli_app = Typer()


@cli_app.command()
def send_meal_message(cj_fresh_meal_store_id: int, slack_webhook_url: str):
    daily_menu = get_today_meal(cj_fresh_meal_store_id)
    sender = slack.MealSummarySender(slack_webhook_url, daily_menu)
    sender.run()


@cli_app.command()
def send_photo_message(cj_fresh_meal_store_id: int, slack_webhook_url: str):
    lunch_options = get_today_lunch_with_image(cj_fresh_meal_store_id)
    sender = slack.LunchWithPhotoSender(slack_webhook_url, lunch_options)
    sender.run()
