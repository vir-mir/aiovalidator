import asyncio
import itertools
import json
import sys
from functools import wraps

from aiovalidator.fields.base import BaseField
from aiovalidator.fields.manager import ManagerField

PY_35 = sys.version_info >= (3, 5)
if PY_35:
    from json import JSONDecodeError
else:
    JSONDecodeError = ValueError

__all__ = ['validator_factory']


def _loads(data):
    try:
        return json.loads(data)
    except JSONDecodeError:
        return {}


def validator_factory(loads=_loads):
    @asyncio.coroutine
    def validator(app, handler):
        if getattr(handler, 'skip_validate', False):
            return handler

        cls_field = getattr(handler, 'Field', None)

        if not cls_field:
            return handler
        else:
            fields = (
                (name, getattr(cls_field, name))
                for name in dir(cls_field)
                if isinstance(getattr(cls_field, name), BaseField)
            )

        load = getattr(handler, 'validator_loads', None) or loads

        @wraps(handler)
        @asyncio.coroutine
        def wrapper(request):
            data = dict(itertools.chain(
                request.match_info.items(),
                request.GET.items(),
                load((yield from request.text())).items()))

            manager = ManagerField(fields, request, data)
            yield from manager.init()
            request['fields'] = manager.manager_dict
            return (yield from handler(request))

        return wrapper

    return validator
