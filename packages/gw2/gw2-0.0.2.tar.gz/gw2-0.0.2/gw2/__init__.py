import re
import requests
from requests.exceptions import HTTPError


class Client(object):

    def __init__(self, baseurl='https://api.guildwars2.com/', version='2'):
        self.baseurl = '{}v{}/'.format(baseurl, version)
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json'})

    def get(self, path, ids=None, **params):
        url = self.baseurl + path
        if isinstance(ids, (list, tuple)):
            ids = ','.join(map(str, ids))
        params['ids'] = ids
        r = self.session.get(url, params=params)
        r.raise_for_status()
        return r.json()

    def auth(self, token):
        self.session.headers.update({'Authorization': 'Bearer {}'.format(token)})
        return self

    def lang(self, lang):
        self.session.headers.update({'Accept-Language': lang})
        return self


uuid_re = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
key_re = re.compile('{0}{0}'.format(uuid_re), re.IGNORECASE)


def find_api_key(text):
    match = key_re.search(text)
    return match.group() if match else None
