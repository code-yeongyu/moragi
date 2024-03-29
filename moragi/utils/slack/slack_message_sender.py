from http import HTTPStatus

from slack_sdk.webhook import WebhookClient
from slack_sdk.webhook.webhook_response import WebhookResponse
from tenacity import retry
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_fixed

from moragi.utils import logger
from moragi.utils.slack.slack_message_builder import SlackMessageBuilder


class SlackMessageSender:

    def __init__(self, url: str, message_builder: SlackMessageBuilder):
        self.url = url
        self.message_builder = message_builder

    @retry(reraise=True, stop=stop_after_attempt(5), wait=wait_fixed(10))
    def run(self):
        webhook = WebhookClient(self.url)
        blocks = self.message_builder.make_slack_blocks()
        logger.debug(f'Sending message to Slack with blocks: {blocks}')
        response: WebhookResponse = webhook.send(
            text='모락이에요!',
            blocks=blocks,
        )
        logger.debug(f'Sent Message to slack with response: {self._webhook_response_to_dict(response)}', )
        if response.status_code != HTTPStatus.OK.value:
            raise Exception(
                f'Error while sending message to slack. response: {self._webhook_response_to_dict(response)}')

    def _webhook_response_to_dict(self, instance: WebhookResponse):
        return {
            'api_url': instance.api_url,
            'status_code': instance.status_code,
            'body': instance.body,
        }
