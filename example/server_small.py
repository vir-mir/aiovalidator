import asyncio
import enum

from aiohttp import web

from aiovalidator import (
    validator_factory,
    middleware_exception,
    IntegerField,
    EnumField
)


async def foo_validator(value):
    await asyncio.sleep(1)
    return value


def foo_default(value):
    async def default():
        return value

    return default


class MyEnum(enum.Enum):
    do = 'do value'
    foo = 'foo value'


class Hello(web.View):
    class Field:
        field1 = IntegerField(validator=foo_validator)
        field2 = IntegerField(default=foo_default(4555555))
        en = EnumField(enum_=MyEnum)

    @asyncio.coroutine
    def get(self):
        fields = self.request['fields']
        print(fields)
        return web.json_response()


app = web.Application(middlewares=[validator_factory(), middleware_exception])
app.router.add_get('/', Hello)
app.router.add_get('/{qwe}/', Hello)
web.run_app(app, port=8000)
