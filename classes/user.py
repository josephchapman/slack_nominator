import os
import requests
import json
import re

LEGACY_TOKEN = os.environ['SLACK_LEGACY_TOKEN']


class User():
    def __init__(self, user_id):
        self.id = user_id


    def names(self):
        # Get names from cache
        with open('member_cache.json', 'r') as infile:
            cached_members = json.load(infile)['Members']

        # Iterate through `cached_members` until ID matches
        # if no matches are found, fallback to API
        for cached_member in cached_members:
            if cached_member['ID'] == self.id:
                username = cached_member['User Name']
                real_name = cached_member['Real Name']
                # Break the for loop
                break
        else:
            users_info = self.api_users_info()
            username = users_info['user']['name']
            real_name = users_info['user']['profile']['real_name']

        return username, real_name


    def api_users_info(self):
        # This API method currently only accepts 'Content-type': 'application/x-www-form-urlencoded',
        #     https://api.slack.com/methods/users.info
        # The requests.get request must therefore use the `params` option to send the payload.
        #     http://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
        headers = {
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': 'Bearer {}'.format(LEGACY_TOKEN)
        }
        payload = {
            'user': self.id
        }
        r = requests.get(
            'https://slack.com/api/users.info',
            headers=headers,
            params=payload
        )
        users_info = json.loads(r.text, encoding='utf-8')
        return users_info


    def presence(self):
        # This data always needs to be fresh
        # No caching here, just straight to API
        users_getPresence = self.api_users_getPresence()
        presence = users_getPresence["presence"]
        return presence


    def api_users_getPresence(self):
        # This API method currently only accepts 'Content-type': 'application/x-www-form-urlencoded',
        #     https://api.slack.com/methods/users.getPresence
        # The requests.get request must therefore use the `params` option to send the payload.
        #     http://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
        headers = {
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': 'Bearer {}'.format(LEGACY_TOKEN)
        }
        payload = {
            'user': self.id
        }
        r = requests.get(
            'https://slack.com/api/users.getPresence',
            headers=headers,
            params=payload
        )
        users_getPresence = json.loads(r.text, encoding='utf-8')
        return users_getPresence


    def status(self):
        # This data always needs to be fresh
        # No caching here, just straight to API
        users_info = self.api_users_info()
        status_emoji = users_info['user']['profile']['status_emoji']
        status_text = users_info['user']['profile']['status_text']

        return status_emoji, status_text


    def remote(self):
        # If the user's status contains any of the `phrases`, `remote` will return `True`
        status_emoji, status_text = self.status()
        phrases = [
            'remote',
            'from home',
            'wfh'
        ]
        emojis = [
            'house',
            'snow-house',
            'house_buildings',
            'house_with_garden'
        ]

        status_match = any(re.search(phrase, status_text, re.IGNORECASE) for phrase in phrases)
        emoji_match = any(re.search(emoji, status_emoji, re.IGNORECASE) for emoji in emojis)

        return status_match or emoji_match
