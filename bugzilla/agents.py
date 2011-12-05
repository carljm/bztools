import os

from bugzilla.models import Bug, BugSearch
from bugzilla.utils import urljoin, qs

class InvalidAPI_ROOT(Exception):
    def __str__(self):
        return "Invalid API url specified. " + \
               "Please set BZ_API_ROOT in your environment " + \
               "or pass it to the agent constructor"

class BugzillaAgent(object):
    def __init__(self, api_root=None, username=None, password=None, http=None):
        self.http = http

        if not api_root:
            api_root = os.environ.get('BZ_API_ROOT')
            if not api_root:
                raise InvalidAPI_ROOT
        self.API_ROOT = api_root

        self.username, self.password = username, password

    def get_bug(self, bug, include_fields='_default,token,cc,keywords,whiteboard', exclude_fields=None, params={}):
        params['include_fields'] = include_fields
        params['exclude_fields'] = exclude_fields

        url = urljoin(self.API_ROOT, 'bug/%s?%s' % (bug, self.qs(**params)))
        return Bug.get(url, http=self.http)

    def get_bug_list(self, params={}):
        url = url = urljoin(self.API_ROOT, 'bug/?%s' % (self.qs(**params)))
        return BugSearch.get(url, http=self.http).bugs

    def qs(self, **params):
        if self.username and self.password:
            params['username'] = self.username
            params['password'] = self.password
        return qs(**params)


class BMOAgent(BugzillaAgent):
    def __init__(self, username=None, password=None, http=None):
        super(BMOAgent, self).__init__('https://api-dev.bugzilla.mozilla.org/latest/', username=username, password=password, http=http)
