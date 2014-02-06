# -*- coding: utf-8 -*-

"""
    Oauth client tailored for the music story API.

    Depends on requests_oauthlib.
"""

import json

from requests_oauthlib import OAuth1Session

class MusicStoryApiError(Exception):
    pass

class MusicStoryOAuthError(MusicStoryApiError):
    """
        Turn the API errors into an nice Python exception.
    """
    def __init__(self, url, **kwargs):
        message = ("[{errorcode}] {type}: {message} "
                   "\n(url was '{url}')").format(url=url, **kwargs)
        super(MusicStoryOAuthError, self).__init__(message)


class MusicStoryOAuth(OAuth1Session):
    """

        Connect to the Music Story API and returns a session object.

        :example:

            >>> oauth_session = MusicStoryOAuth(consumer_key, client_secret=consumer_secret)
            >>> oauth_session.fetch_request_token(request_token_url)
            >>> res = oauth_session.get('http://api.music-story.com/artist/search.json?name=Bob%20Marley')
            >>> print res.content

        Works only with the JSON API
    """

    def _fetch_token(self, url):
        """
            Extract auth token from their response.

            Wrap any or their API error in a Python exception.s
        """
        text = self.post(url).text

        try:
            response = json.loads(text)
        except ValueError:
            raise MusicStoryApiError(
                "Unable to decode JSON from %s. Check you are not using the "
                "XML API and that the request is well formatted."
            )

        if response['code'] != 0:
            raise MusicStoryOAuthError(url, **response['error'])

        token = {}
        for key, val in response['data'].items():
            token['oauth_' + key] = val
        self._populate_attributes(token)
        return token

