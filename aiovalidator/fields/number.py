from typing import Union

from .base import BaseField
from ..middlewares import abort

__all__ = ['IntegerField', 'FloatField', 'BoolField']


class IntegerField(BaseField):
    def get_value(self, value: Union[int, str, float]) -> int:
        """

        :param value: external value
        :raise: HTTPExceptionJson
        """
        try:
            return int(value)
        except (ValueError, TypeError):
            raise abort(status=406,
                        text='Field {} is not integer'.format(self.name))


class FloatField(BaseField):
    def get_value(self, value: Union[int, str, float]) -> float:
        """

        :param value: external value
        :raise: HTTPExceptionJson
        """
        try:
            return float(value)
        except (ValueError, TypeError):
            raise abort(status=406,
                        text='Field {} is not float'.format(self.name))


class BoolField(IntegerField):
    def get_value(self, value: Union[int, str, float]) -> bool:
        """

        :param value: external value
        :raise: HTTPExceptionJson
        """
        return bool(value)
