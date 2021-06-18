import os
import requests
import json

LEGACY_TOKEN = os.environ['SLACK_LEGACY_TOKEN']


class Channel():
    def __init__(self, channel_id):
        self.id = channel_id

    def members(self):
        conversations_members = self.api_conversations_members()
        members = conversations_members['members']
        return members

    def api_conversations_members(self):
        # This API method currently only accepts 'Content-type': 'application/x-www-form-urlencoded',
        #     https://api.slack.com/methods/conversations.members
        # The requests.get request must therefore use the `params` option to send the payload.
        #     http://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
        headers = {
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': 'Bearer {}'.format(LEGACY_TOKEN)
        }
        payload = {
            'channel': self.id
        }
        r = requests.get(
            'https://slack.com/api/conversations.members',
            headers=headers,
            params=payload
        )
        conversations_members = json.loads(r.text, encoding='utf-8')
        return conversations_members
