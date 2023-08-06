# coding: utf-8
import logging
from string import Template

import requests


DEFAULT_TITLE = 'Sentinel Notification'
DEFAULT_MESSAGE = 'The value "$value" broke the rule $rule'

class Pushbullet:
    def __init__(self, access_token,
                 title=DEFAULT_TITLE, message=DEFAULT_MESSAGE):
        """Set your pushbullet configurations.

        Parameters
        ----------
        access_token : str
            Your access token can be found on the Account Settings.
        title : str
            Notification title
        message : str
            Optional placeholders: $rule $value

        """
        self._access_token = access_token
        self._title = title
        self._message = Template(message)

    def send(self, payload, rule):
        """Send a push notification.

        Parameters
        ----------
        msg : str
            Your access token can be found on the Account Settings.
        payload : :obj:`bytes`
            MQTT payload received
        rule : :obj:`Rule()`
            Broken rule

        """
        message = self._message.safe_substitute(
            rule=str(rule), value=payload.decode())

        r = requests.post(
            'https://api.pushbullet.com/v2/pushes',
            headers={'Access-Token': self._access_token},
            json={
                'title': self._title, 'body': message, 'type': 'note'
            })

        if r.status_code != 200:
            logging.error(r.text)
