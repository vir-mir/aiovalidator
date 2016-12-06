from .base import BaseField
from ..middlewares import abort

__all__ = ['IntegerField', 'FloatField', 'BoolField']


class IntegerField(BaseField):
    def get_value(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            raise abort(status=406,
                        text='Field {} is not integer'.format(self.name))


class FloatField(BaseField):
    def get_value(self, value):
        try:
            return float(value)
        except (ValueError, TypeError):
            raise abort(status=406,
                        text='Field {} is not float'.format(self.name))


class BoolField(IntegerField):
    def get_value(self, value):
        return bool(value)
