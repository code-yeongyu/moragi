from typer import Typer

from moragi.utils import cj_fresh_meal, slack

app = Typer()


@app.command()
def get_meals_and_send_message(cj_fresh_meal_store_id: int, slack_webhook_url: str):
    options = cj_fresh_meal.get_food_options(cj_fresh_meal_store_id)
    breafast_options = options['1']
    lunch_options = options['2']
    slack.send_slack_message(slack_webhook_url, breafast_options, lunch_options)


@app.command()
def get_photos_and_send_message(cj_fresh_meal_store_id: int, slack_webhook_url: str):
    options = cj_fresh_meal.get_food_options(cj_fresh_meal_store_id)
    breafast_options = options['1']
    lunch_options = options['2']
    slack.send_slack_message(slack_webhook_url, breafast_options, lunch_options)
