import os
import json
import datetime

from classes.channel import *
from classes.user import *


# Methods:
#   settings_read()
#   read()
#   write(data)
#   flush()
#   update()
#   _update(channel, cache_data)



class Cache():
    def __init__(self):
        self.settings_file = 'settings.json'
        self.cache_file = 'member_cache.json'


    def settings_read(self):
        with open(self.settings_file, 'r') as infile:
            settings_data = json.load(infile)
        return settings_data


    def read(self):
        with open(self.cache_file, 'r') as infile:
            cache_data = json.load(infile)
        return cache_data


    def write(self, data):
        with open(self.cache_file, 'w') as outfile:
            json.dump(data, outfile, indent=2)


    def flush(self):
        # Remove data from `member_cache_file`

        print('Flushing cache...')

        # Create the (flushed) dictionary
        flushed_data = {
            'Latest Update': '',
            'Latest Flush': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Channel': '',
            'Members': []
        }

        # Write the dictionary to the cache file
        self.write(flushed_data)
        return flushed_data


    def update(self):
        # This method is a wrapper around `_update()`
        # It reads the settings and cache,
        #   then passes the required data to `_update()`

        # Read settings file: `settings.json`
        settings_data = self.settings_read()
        # Read cache file: `member_cache.json`
        cache_data = self.read()

        # Update cache
        self._update(settings_data['Settings']['Channel Scan'], cache_data)
        return None


    def _update(self, channel, cache_data):

        print('Updating cache with data from channel: {}...'.format(channel))

        # Instantiate channel and load current members from Slack API
        channel_obj = Channel(channel)
        current_members = channel_obj.members()
        cached_members = cache_data['Members']

        # List records in the cache that aren't in the current member list
        print('Finding stale cache entries...')
        removals = []
        for cached_member in cached_members:
            if cached_member['ID'] not in current_members:
                removals.append(cached_member)

        if len(removals) > 0:
            print('Removing the following entries that were found in the cache file, but not the channel:\n{}'.format(str(json.dumps(removals, indent=2))))
        else:
            print('No stale entries in cache for removal.')

        # Perform the removals
        for removal in removals:
            cached_members.remove(removal)


        # List records in the current member list that aren't in the cache
        print('Finding new channel entries...')
        additions = []
        for current_member in current_members:
            if current_member not in [cached_member['ID'] for cached_member in cached_members]:
                addition_obj = User(current_member)
                username, real_name = addition_obj.names()
                addition = {'Real Name': real_name, 'User Name': username, 'ID': current_member}
                additions.append(addition)

        if len(additions) > 0:
            print('Adding the following entries that were found in the channel, but not the cache file:\n{}'.format(str(json.dumps(additions, indent=2))))
        else:
            print('No new entries in channel for addition.')

        # Perform the additions
        for addition in additions:
            cached_members.append(addition)

        # Create the (updated) dictionary
        updated_data = {
            'Latest Update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Latest Flush': cache_data['Latest Flush'],
            'Channel': channel,
            'Members': cached_members
        }

        # Write the dictionary to the cache file
        self.write(updated_data)
        return updated_data
