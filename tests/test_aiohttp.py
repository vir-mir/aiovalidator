import asyncio
import json

import pytest
from aiohttp import web

from aiovalidator import (
    IntegerField,
    middleware_exception,
    validator_factory,
    abort)


@asyncio.coroutine
def foo_validator_async(value):
    return value * 2


def foo_default_async(value):
    @asyncio.coroutine
    def default():
        return value * 2

    return default


def foo_default(value):
    def default():
        return value * 2

    return default


class ViewTest(web.View):
    class Field:
        user_id = IntegerField()
        field1 = IntegerField(methods={'GET', 'POST'},
                              validator=foo_validator_async)
        field1_async = IntegerField(validator=(lambda x: x * 2))

        field2 = IntegerField(default=foo_default_async(6), methods={'GET'})
        field2_async = IntegerField(default=foo_default(6))
        field4 = IntegerField(default=123)

    @asyncio.coroutine
    def get(self):
        return web.json_response(self.request['fields'])

    @asyncio.coroutine
    def post(self):
        return web.json_response(self.request['fields'])

    @asyncio.coroutine
    def put(self):
        return web.json_response(self.request['fields'].user_id)


class ViewTestSkip(web.View):
    skip_validate = True

    class Field:
        user_id = IntegerField(default=0)

    @asyncio.coroutine
    def get(self):
        return web.json_response(None)


class ViewTestNotField(web.View):
    @asyncio.coroutine
    def get(self):
        return web.json_response(None)


class ViewTestAbort(web.View):
    @asyncio.coroutine
    def get(self):
        raise abort(status=406, text='error')


@pytest.fixture
def cli(loop, test_client):
    app = web.Application(loop=loop,
                          middlewares=[validator_factory(),
                                       middleware_exception])
    app.router.add_route('*', '/skip', ViewTestSkip)
    app.router.add_route('*', '/not_field', ViewTestNotField)
    app.router.add_route('*', '/abort', ViewTestAbort)
    app.router.add_route('*', '/{user_id}', ViewTest)
    return loop.run_until_complete(test_client(app))


@asyncio.coroutine
def test_client_field(cli):
    resp = yield from cli.get('/123?field1=6&field1_async=6')
    assert (yield from resp.json()) == {
        'user_id': 123,
        'field1': 12,
        'field1_async': 12,
        'field2': 12,
        'field2_async': 12,
        'field4': 123,
    }


@asyncio.coroutine
def test_client_field_post(cli):
    data = {
        'field1_async': 2,
        'field4': 5
    }
    resp = yield from cli.post('/123?field1=6', data=json.dumps(data))

    assert (yield from resp.json()) == {
        'user_id': 123,
        'field1': 12,
        'field1_async': 4,
        'field2_async': 12,
        'field4': 5,
    }


@asyncio.coroutine
def test_client_field_put(cli):
    resp = yield from cli.put('/123?field1=6&field1_async=6')
    assert (yield from resp.json()) == 123


@asyncio.coroutine
def test_client_field_skip(cli):
    resp = yield from cli.get('/skip')
    assert (yield from resp.json()) is None


@asyncio.coroutine
def test_client_field_not_field(cli):
    resp = yield from cli.get('/not_field')
    assert (yield from resp.json()) is None


@asyncio.coroutine
def test_client_field_required(cli):
    resp = yield from cli.get('/123')
    assert (yield from resp.json()) == {'message': 'Field field1 required'}
    resp = yield from cli.get('/123?field1=123')
    assert (yield from resp.json()) == {
        'message': 'Field field1_async required'}


@asyncio.coroutine
def test_client_field_abort(cli):
    resp = yield from cli.get('/abort')
    assert (yield from resp.json()) == {'message': 'error'}
