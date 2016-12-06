import asyncio
import json
from functools import wraps

from aiohttp import web
from aiohttp.web import HTTPException

__all__ = ['middleware_exception', 'abort']


@asyncio.coroutine
def middleware_exception(app, handler):
    @wraps(handler)
    @asyncio.coroutine
    def middleware_handler(request):
        try:
            return (yield from handler(request))
        except HTTPException as e:
            if not isinstance(e, HTTPExceptionJson):
                return HTTPExceptionJson(status_code=e.status,
                                         text=e.reason)
            return e

    return middleware_handler


def abort(*, status, text):
    if type(text) is not [dict, list]:
        text = {
            'message': text
        }

    return HTTPExceptionJson(status_code=status, text=text, headers={
        'Content-Type': 'application/json'
    })


class HTTPExceptionJson(HTTPException):
    status_code = None
    empty_body = False

    def __init__(self, *, status_code=None, headers=None, reason=None,
                 body=None, text=None, content_type=None):
        self.status_code = status_code
        if type(text) is str:
            text = {'message': text}
        text = json.dumps(text)
        web.Response.__init__(self, status=self.status_code,
                              headers=headers, reason=reason,
                              body=body, text=text, content_type=content_type)
        Exception.__init__(self, self.reason)
