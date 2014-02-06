# -*- coding: utf-8 -*-


from __future__ import unicode_literals, absolute_import

from itertools import islice
from collections import namedtuple

from .exceptions import APIError


class Context(namedtuple('Context', ['api', 'url', 'params'])):
    def __new__(cls, api, url, params=None):
        return super(Context, cls).__new__(cls, api, url, params)


class QuerySet(object):

    def __init__(self, subject, context):
        self.context = context
        self.subject = subject
        self.is_loaded = False


    def __len__(self):
        if not self.is_loaded:
            self.load()
        return int(self.count)

    def __unicode__(self):
        return self.__repr__()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<MusicStory%sQueryset>" % self.subject.title()


    def page(self, page):
        if page < 1:
            raise ValueError('Page cannot be negative')
        self.context.params['page'] = int(page)
        self.load()
        return self


    def load(self):
        self.is_loaded = True
        api, url, params = self.context
        data = api.session.get(url, params=params).json()

        if data['code'] < 0:
            raise APIError(data)

        return self.load_json(data)


    def load_json(self, data):
        self.data = data
        self.count = data['count']
        self.page = data['currentPage']
        self.page_count = data['pageCount']
        return self


    @property
    def has_next(self):
        return self.page < self.page_count


    @property
    def has_previous(self):
        return self.page != 1


    def next(self):
        api, url, params = self.context
        params['page'] = params.get('params', self.page) + 1
        self.context = Context(api, url, params)
        self.load()


    def previous(self):
        api, url, params = self.context
        params['page'] = params.get('params', self.page) - 1
        self.context = Context(api, url, params)
        self.load()


    def __getitem__(self, i):
        if not self.is_loaded:
            self.load()

        if isinstance(i, slice):
            return islice(self, i.start, i.stop)

        return MusicStoryObject(self.subject,
                                self.data['data'][i],
                                self.context.api)


    def __iter__(self):

        while True:
            for obj in self.iter_page():
                yield obj

            if not self.has_next:
                break

            self.next()


    def iter_page(self):

        if not self.is_loaded:
            self.load()

        for entry in self.data['data']:
            yield MusicStoryObject(self.subject, entry, self.context.api)




class MusicStoryObject(object):
    """
        Represents a entry from the MusicStory API.

        Allows to ask for connectors using the connector() method.
    """

    id = 'unknow'

    def __init__(self, object_name, data, api):
        self.object_name = object_name
        self.fields = data.keys()
        self.api = api
        self.__dict__.update(data)
        self._cache = {}

    def connector(self, object_name, force=False, lang=None, **kwargs):
        """
            Fetch the given connector and returns a queryset for it.

            The result will be cached in the current instance so next calls
            to this methods won't make an API call unless you pass `force` as
            True.
        """

        lang = lang or self.api.DEFAULT_LANG
        if force or object_name not in self._cache:
            url = self.api.url('connector', subject=self.object_name, id=self.id,
                               connector=object_name, lang=lang)
            ctx = Context(self.api, url, params=kwargs)
            self._cache[object_name] = QuerySet(object_name, ctx)

        return self._cache[object_name]


    def __unicode__(self):
        return self.__repr__()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<MusicStory%s id=%s>" % (self.object_name.title(), self.id)
