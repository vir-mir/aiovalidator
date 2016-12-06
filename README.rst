aiovalidator
============
.. image:: https://travis-ci.org/vir-mir/aiovalidator.svg?branch=master
    :target: https://travis-ci.org/vir-mir/aiovalidator
.. image:: https://codecov.io/gh/vir-mir/aiovalidator/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/vir-mir/aiovalidator


Example
-------

::

    import asyncio

    from aiohttp import web

    from aiovalidator import (
        validator_factory,
        middleware_exception,
        IntegerField
    )


    async def foo_validator(value):
        await asyncio.sleep(1)
        return value


    def foo_default(value):
        async def default():
            return value

        return default


    class Hello(web.View):
        class Field:
            field1 = IntegerField()
            field2 = IntegerField(required=False, methods={'GET'},
                                  verbose_name='Field method get')
            field3 = IntegerField(validator=foo_validator, )
            field4 = IntegerField(default=foo_default)

        @asyncio.coroutine
        def get(self):
            fields = self.request['fields']
            print(fields)
            return web.json_response()


    app = web.Application(middlewares=[validator_factory(), middleware_exception])
    app.router.add_get('/{user_id}/', Hello)
    web.run_app(app, port=8000)


My fields example
-----------------

::

    import phonenumbers
    from aiovalidator import StrField, abort


    class PhoneField(StrField):
        def get_value(self, value):
            value = super().get_value(value)
            try:
                value = phonenumbers.parse(value, 'RU')
                region = phonenumbers.region_code_for_number(value)
                regions = phonenumbers.COUNTRY_CODE_TO_REGION_CODE[7]
                if not phonenumbers.is_valid_number(value):
                    abort(status=400,
                          text='Field {} not format phone'.format(self.name))
                if region not in regions:
                    abort(status=400,
                          text='Field {} not format phone'.format(self.name))
                value = phonenumbers.format_number(
                    value, phonenumbers.PhoneNumberFormat.E164
                )[1:]

                return value
            except phonenumbers.NumberParseException:
                abort(status=400, text='Field {} not valid'.format(self.name))
