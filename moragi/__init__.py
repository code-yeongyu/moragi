from time import sleep

from typer import Typer

from moragi.utils import cj_fresh_meal, console, slack

app = Typer()


@app.command()
def send_meal_message(cj_fresh_meal_store_id: int, slack_webhook_url: str):
    options = cj_fresh_meal.get_food_options(cj_fresh_meal_store_id)
    breafast_options = options['1']
    lunch_options = options['2']
    slack.send_meal_message(slack_webhook_url, breafast_options, lunch_options)


@app.command()
def send_photo_message(cj_fresh_meal_store_id: int, slack_webhook_url: str):
    options = _get_food_with_image(cj_fresh_meal_store_id)
    lunch_options = options['2']
    slack.send_photo_message(slack_webhook_url, lunch_options)


def _get_food_with_image(cj_fresh_meal_store_id: int):
    MAX_TRY = 3
    for i in range(1, MAX_TRY):
        options = cj_fresh_meal.get_food_options(cj_fresh_meal_store_id)
        lunch_first_option_thumbnail = options['2'][0].thumbnail_url
        if lunch_first_option_thumbnail:
            return options
        with console.status(f'No image found. Retrying in 10 minutes ... [{i}/{MAX_TRY}]'):
            sleep(60 * 10)
    raise Exception('No image found')
