import datetime

from .number import IntegerField
from .string import StrField
from ..middlewares import abort

__all__ = ['DateTimeField', 'DateField', 'TimeStampField']


class DateTimeField(StrField):
    def __init__(self, format_='%Y-%m-%d %H:%M:%S', **kwargs):
        self.format = format_
        super().__init__(**kwargs)

    def get_value(self, value):
        try:
            return datetime.datetime.strptime(value, self.format)
        except ValueError:
            raise abort(status=406,
                        text='Field {} is not date time format, {}'.format(
                            self.name, self.format))


class DateField(DateTimeField):
    def __init__(self, format_='%Y-%m-%d', **kwargs):
        super().__init__(format_, **kwargs)

    def get_value(self, value):
        value = super().get_value(value)
        return value.date()


class TimeStampField(IntegerField):
    def get_value(self, value):
        value = super().get_value(value)
        return datetime.datetime.fromtimestamp(value)
