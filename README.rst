Music Story Python SDK
=======================

Version : 0.1
For Python : 2.7 and 3.3
Licence: BSD

The SDK written allows a simplified use of the API Music Story (developers.music-story.com).

It provides basis functionalities such as the Oauth authentification, the search and retrieval of Objects, connectors, and the exploration of results.

It can also serve as a basis for the development of libraries with more advanced functionalities.


Setup
------

If you have pip available, installing is as simple as::

    pip install music_story

Otherwise you can extract the source code and to:

    python setup.py install

You'll need internet for the installer to download the dependancies.


Authentication
--------------

The authentication is done during the instancing of the MusicStoryAPI class.
It is necessary in order to identify yourself to provide your "consumer_key" and "consumer_secret" keys.

If you don't specify your access tokens: "token" and "token_secret", the authentication will take care of getting new ones.


Example::

    # First connection
    api = MusicStoryApi('you key here', 'your secret here')
    api.connect()

    token = api.token
    token_secret = api.token_secret

    # save this for later usage, then on next connection :
    api = MusicStoryApi('you key here', 'your secret here', token, token_secret)
    api.connect()



Retrieval of an object by an ID
---------------------------------

The function that allows this operation is the function::

    api.get(object_name, object_id)

Refer to the online documentation (developers.music-story.com/developers) to know the list of Music Story objects available.

Example::

    # retrieval of the genre with the ID 66
    genre = api.get("genre", 66)
    print(genre.name)
    ## Electro

The object sent back will be an instance of the "MusicStoryObject" class.

The data of the data retrieved will be accessible as regular attributs. You
can lookup for all the attributes names available as API data using
the `fields` attributs. It's only available AFTER you made the query.

You can specify you need editorial fields by listing them in `editorial_fields`::

    artist = api.get("artist", id=1, editorial_fields=['country'])
    print(artist.country)
    ## England

You may also specify the language code of the lang you want to get the results in::

    artist = api.get("artist", id=1, editorial_fields=['country'], lang='fr')

But be aware the API as some fields that are not available in other languages
than the default (english).


Search for the objects
-----------------------

The search for objects is done via the method::

api.search(object_name, **filters)

Filters are listed in the MusicStoryAPI doc, and can be text patterns or date
intervals.

By default the number of results per page is 10 and is fixed as a maximum of 100.

Example:

    # search for the album versions which includes the word
    # "love" in the name and is of the "live" type
    releases = api.search('release', type='Live', title='love')

    # get the first result in the list :
    rel = releases[0] # get item 0 from the current page
    print(rel.id)
    ## "228095"
    print(releases.page)
    ## 1

    # results are iterable queryset...
    r1, r2, r3 = releases[12:15]
    print(r1.title)
    ## Such Is Love

    # ...but be aware it will make queries every time it needs to paginate !
    # So you can make this and iterate thought the whole queryset :
    for release in releases:
        print(r1.title)
    # And it will paginate automatically for you, but will need to make a query
    # for each new page it loads.


Some explicit methods are put at your disposition such as the iterator functions "next()", "prev()","hasNext()","hasPrev()" if you want to controle pagination manually.


Connectors
-----------

It is possible to carry out a request of the connector type on a "MusicStoryObject" by using the method::

    api.connector(object_name, **filters)

Refer to the online documentation (developers.music-story.com/developers) to know the list of connectors of the available object.

The result is of the same type as for a search request::

    genre = api.get('genre', 64)
    artistes = genre.connector('artists', name='Tommy')
    print(artistes[0].name)
    ## Tommy Bolin
