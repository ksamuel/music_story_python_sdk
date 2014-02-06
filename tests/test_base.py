# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

import os
import pytest
import tempfile

CREDENTIALS_FILE = os.path.join(tempfile.gettempdir(), "musicstory-test-credential")

from music_story import MusicStoryApi


@pytest.fixture
def credentials():
    creds = {}
    with open(CREDENTIALS_FILE) as f:
        for line in f:
            key, val = line.split('=')
            creds[key.strip()] = val.strip()
    return creds


@pytest.fixture
def api(credentials):
    key = credentials['consumer_key']
    secret = credentials['consumer_secret']
    token = credentials.get('access_token')
    token_secret = credentials.get('token_secret')
    return MusicStoryApi(key, secret, token, token_secret).connect()


def test_connect(api):
    genre = api.get("genre", 66)
    assert genre.name == "Electro"


def test_editorial_fields(api):
    artist = api.get("artist", id=1, editorial_fields=['country'])
    assert artist.country == 'England'

    artist = api.get("artist", id=1, editorial_fields=['country'], lang='fr')
    assert artist.country == None


def test_search(api):
    releases = api.search('release', type='Live', title='love')

    rel = releases[0]
    assert rel.id == "228095"

    r1, r2, r3 = releases[12:15]
    assert "Love" in r1.title

def test_connector(api):

    genre = api.get('genre', 64)
    artistes = genre.connector('artists', name='Tommy')
    assert artistes[0].name == 'Tommy Bolin'

