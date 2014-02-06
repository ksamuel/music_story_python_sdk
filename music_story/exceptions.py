# -*- coding: utf-8 -*-



class APIError(Exception):

    def __init__(self, data, *args, **kwargs):
        error = data['error']
        super(APIError, self).__init__(error.pop('message'), *args, **kwargs)
        self.__dict__.update(error)