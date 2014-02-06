# -*- coding: utf-8 -*-


from __future__ import unicode_literals, absolute_import


from .models import Context, QuerySet, MusicStoryObject
from .music_story_oauth import MusicStoryOAuth
from .exceptions import APIError


class MusicStoryApi(object):
    """
        Main class to manipulate the MusicStory API.

        Use connect() to create a session, then get() and search() to query
        the API.
    """

    URLS = {
        'fetch_token': '/oauth/request_token.json',
        'search': '/{lang}/{subject}/search.json',
        'get': '/{lang}/{subject}/{id}.json',
        'connector': '/{lang}/{subject}/{id}/{connector}.json',
    }

    DEFAULT_LANG = 'en'
    BASE_URL = 'http://api.music-story.com'


    def __init__(self, consummer_key, consummer_secret,
                       token=None, token_secret=None):
        """
            Standard Oauth 1 parameters. if you don't pass token(_secret),
            it will request new ones for you.
        """
        self.consummer_key = consummer_key
        self.consummer_secret = consummer_secret
        self.token = token
        self.token_secret = token_secret


    def url(self, name, lang=None, **kwargs):
        """
            Create a valid API URL using the class URLS mapping and parameters.
        """
        lang = lang or self.DEFAULT_LANG
        return self.BASE_URL + self.URLS[name].format(lang=lang, **kwargs)



    def connect(self):
        """
            Oauth 1 connection using the parameters passed via __init__.

            Returns itself for method chaining.
        """
        if not self.token or self.token_secret:
            session = MusicStoryOAuth(self.consummer_key,
                                      client_secret=self.consummer_secret)
            response = session.fetch_request_token(self.url('fetch_token'))

            self.token = response["oauth_token"]
            self.token_secret = response["oauth_token_secret"]

        self.session = MusicStoryOAuth(self.consummer_key,
                                       client_secret=self.consummer_secret,
                                       resource_owner_key=self.token,
                                       resource_owner_secret=self.token_secret)

        return self


    def search(self, subject, lang=None, **kwargs):
        """
            Query the API for a list of objects matching the parameters.

            Returns a lazy QuerySet you can iterate on.
        """
        url = self.url('search', subject=subject, lang=lang or self.DEFAULT_LANG)
        return QuerySet(subject, Context(self, url, kwargs))


    def get(self, subject, id, editorial_fields=(), **kwargs):
        """
            Query the API for a particular object matching the given ID.

            Returns a MusicStoryObject.
        """
        url = self.url('get', subject=subject, id=id, **kwargs)
        params = {}
        if editorial_fields:
            params['fields'] = ','.join(editorial_fields)

        data = self.session.get(url, params=params).json()

        if data['code'] < 0:
            raise APIError(data)

        return MusicStoryObject(subject, data, self)

