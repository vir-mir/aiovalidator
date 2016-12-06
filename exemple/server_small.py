import asyncio

from aiohttp import web

from aiorest_validator import (
    validator_factory,
    middleware_exception,
    IntegerField
)


async def foo(value):
    await asyncio.sleep(3)
    return value


def foo2(value):
    async def foo22():
        return value

    return foo22


class Hello(web.View):
    class Field:
        qwe = IntegerField(validator=foo)
        asds = IntegerField(default=foo2(4555555))

    @asyncio.coroutine
    def get(self):
        fields = self.request['fields']
        print(fields)
        return web.json_response(fields)


app = web.Application(middlewares=[validator_factory(), middleware_exception])
app.router.add_get('/', Hello)
app.router.add_get('/{qwe}/', Hello)
web.run_app(app, port=8000)
