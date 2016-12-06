import asyncio

from ..middlewares import abort


class ManagerDict(dict):
    __slots__ = ()

    def __getattr__(self, name):
        return self[name]


class ManagerField:
    __slots__ = ('_fields', '_request', 'manager_dict', '_data')

    def __init__(self, fields, request, data):
        self._fields = fields
        self._request = request
        self._data = data
        self.manager_dict = ManagerDict()

    @asyncio.coroutine
    def init(self):
        fields = ((name, field) for name, field in self._fields
                  if self._request.method in field.methods)

        data = self._data
        manager_dict = self.manager_dict

        for name, field in fields:
            field.name = name

            if name in data:
                val = field._get_value(data[name])
            elif field.required is False:
                val = field.default()
            else:
                raise abort(status=406, text='Field {} required'.format(name))

            if asyncio.iscoroutine(val):
                manager_dict[name] = yield from val
            else:
                manager_dict[name] = val
