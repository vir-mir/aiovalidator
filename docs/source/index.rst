.. aiovalidator documentation master file, created by
   sphinx-quickstart on Thu Dec  8 14:08:25 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

aiovalidator: addition aionttp validation/building restful api
===============================================================

Features
--------

- Easily integrates with `phonenumbers`, `trafaret` and other libraries
- It allows to process data async
- You can quickly expand your field to check
- Ability to exclude the views of the processing
- Ability to change the processing driver json, xml ...


Library Installation
--------------------

.. code-block:: bash

    $ pip install aiovalidator


Getting Started
---------------
Example::

    import asyncio
    import enum

    from aiohttp import web

    from aiovalidator import (
        validator_factory,
        middleware_exception,
        IntegerField,
        EnumField,
        StrField
    )


    async def foo_validator(value):
        assert isinstance(value, int)
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
            field2 = StrField(default=foo_default('default string'))
            en = EnumField(enum_=MyEnum)

        @asyncio.coroutine
        def get(self):
            fields = self.request['fields']
            print(fields)
            return web.json_response()


    app = web.Application(middlewares=[validator_factory(),
                                       middleware_exception])
    app.router.add_get('/', Hello)
    web.run_app(app, port=8000)



Contents
--------
.. toctree::
    fields
    contributing




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
