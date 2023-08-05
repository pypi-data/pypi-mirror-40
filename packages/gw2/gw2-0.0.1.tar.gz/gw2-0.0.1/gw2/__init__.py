import re
import requests


class Client:

    def __init__(self, baseurl='https://api.guildwars2.com/', version='2', token=None):
        self.baseurl = '{}v{}/'.format(baseurl, version)
        self.token = token

    def get(self, path, token=None, headers=None, **kwargs):
        headers = headers or {}
        token = token or self.token
        if token:
            headers['Authorization'] = 'Bearer {}'.format(token)
        r = requests.get(self.baseurl + path, headers=headers, **kwargs)
        r.raise_for_status()
        return r.json()


uuid_re = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
key_re = re.compile('{0}{0}'.format(uuid_re), re.IGNORECASE)


def find_api_key(text):
    match = key_re.search(text)
    return match.group() if match else None
