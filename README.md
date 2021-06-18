# Slack Nominator

Python script to interact with Slack API.  
Selects a random user from a specified Slack channel based on a list of inclusions and their activity/status, then messages the specified channel nominating them to do something.  
Written for Python 3.5


## Instructions

These instructions are written for Ubuntu 16.04.  Adjust as necessary.

* **[Optional]** Create and activate a `venv` (in a suitable location), then upgrade `pip3` within the new `venv`:
```
$ python3 -m venv slack_nominator
$ source slack_nominator/bin/activate
(slack_nominator) $ pip3 install --upgrade pip
```

* **[Required]** Install requirements:
```
(slack_nominator) $ pip3 install -r requirements.txt
```

* **[Required]** Rename or duplicate these files as follows:  
    `settings_sample.json` -> `settings.json`  
    `member_cache_sample.json` -> `member_cache.json`

* **[Required]** Populate `settings.json` with your required settings

* **[Required]** Export your Slack legacy token to your current shell (add to your shell's run commands file (e.g. `bashrc`) to export on startup):
```
(slack_nominator) $ export SLACK_LEGACY_TOKEN=xoxp-1111111111-22222222222-333333333333-0123456789abcdef0123456789abcdef
```

* **[Optional]** Schedule a cron (note: `.bashrc` will need sourcing for cron's shell):
```
0 8 * * 1-5 . /path/to/.bashrc; /path/to/venv/bin/python3 /path/to/slack_nominator/slack_nominator.py
```

## Regular operation

Run the script with no options to perform the whole script:
```
(slack_nominator) $ python3 slack_nominator.py
```

See `help` menu for options to run individual sections of the script:
```
(slack_nominator) $ ./slack_nominator.py -h
usage: slack_nominator.py [-h] [-f] [-u] [-s]

optional arguments:
  -h, --help    show this help message and exit
  -f, --flush   flush the cache
  -u, --update  update the cache
  -s, --select  select someone
```
