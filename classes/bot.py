import os
import requests
import json
import datetime
from random import shuffle

from classes.user import *
from classes.cache import *

LEGACY_TOKEN = os.environ['SLACK_LEGACY_TOKEN']

# Methods:
#   settings_read()
#   select()
#   _select(cached_members, inclusions)
#   post_message(channel, message)
#   assign()

class Bot():
    def __init__(self):
        self.settings_file = 'settings.json'
        self.cache = Cache()    # Instantiate the cache


    def settings_read(self):
        with open(self.settings_file, 'r') as infile:
            settings_data = json.load(infile)
        return settings_data


    def select(self):
        # This method is a wrapper around `_select()`
        # It reads the settings and cache,
        #   then passes the required data to `_select()`

        # Read cache file: `member_cache.json`
        cache_data = self.cache.read()
        # Read settings file: `settings.json`
        settings_data = self.settings_read()

        # Select a member from inclusions, using cached data for details
        selected_member_obj = self._select(cache_data['Members'], settings_data['Inclusions'])

        return selected_member_obj


    def _select(self, cached_members, inclusions):
        # Returns a `User` object (or None) from a list of `inclusions` based on attributes.
        # The `cached_members` data is used to translate between `Real Name` and `ID`

        # Turn `inclusions` into list of IDs
        members = [cached_member['ID'] for cached_member in cached_members if cached_member['Real Name'] in inclusions]

        # Shuffle the member IDs from cache
        shuffle(members)

        # Check they're included and active
        # but not remote
        for member in members:
            member_obj = User(member)
            if (
                member_obj.presence() == 'active' and
                not member_obj.remote()
            ):
                print('Selected Member: {}'.format(str(member_obj.names())))
                return member_obj
        else:
            print('Selected Member: NONE FOUND')
            return None


    def post_message(self, channel, message):
        # As of October 2017, this API method accepts 'Content-type': 'application/json',
        #     https://api.slack.com/methods/chat.postMessage
        #     https://api.slack.com/changelog/2017-10-keeping-up-with-the-jsons
        # The requests.post request can therefore use the `json` option to send the payload.
        #     http://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
        # `json` option requires requests version 2.4.2.  Run `pip show requests` to view installed version.
        headers = {
            'Content-type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer {}'.format(LEGACY_TOKEN)
        }
        payload = {
            'channel': channel,
            'text': message,
            'as_user': 'false',
            'username': 'Slack Nominator',
            'icon_emoji': ':game_die:'
        }
        r = requests.post(
            'https://slack.com/api/chat.postMessage',
            headers=headers,
            json=payload
        )
        return r.text


    def assign(self):
        # Read settings file: `settings.json`
        settings_data = self.settings_read()

        cache_data = self.cache.read()

        # Convert timestamps in the cache file to datetime objects
        latest_flush_strp = datetime.datetime.strptime(cache_data['Latest Flush'], '%Y-%m-%d %H:%M:%S')
        latest_update_strp = datetime.datetime.strptime(cache_data['Latest Update'], '%Y-%m-%d %H:%M:%S')

        # if it's Monday and cache wasn't already flushed today
        if (
            datetime.date.today().weekday() == 0 and
            not latest_flush_strp.date() == datetime.datetime.now().date()
        ):
            self.cache.flush()

        # Update cache
        cache_data = self.cache._update(settings_data['Settings']['Channel Scan'], cache_data)

        # Select member
        selected_member_obj = self._select(cache_data['Members'], settings_data['Inclusions'])

        action = 'take notes in the huddle today'

        # Post message
        if selected_member_obj:
            user_id = selected_member_obj.id
            username, real_name = selected_member_obj.names()
            message = '{0} (<@{1}>) has been randomly selected to {2}'.format(real_name, user_id, action)
            print(message)
            response = self.post_message(settings_data['Settings']['Channel Post'], message)
            print ('Response: {}\n'.format(response))
        else:
            message = 'I failed to find a valid user to {}'.format(action)
            print(message)
            response = self.post_message(settings_data['Settings']['Channel Post'], message)
            print ('Response: {}\n'.format(response))
