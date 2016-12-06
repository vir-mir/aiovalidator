import enum

from .base import BaseField
from ..middlewares import abort

__all__ = ['StrField', 'EnumField']


class StrField(BaseField):
    def get_value(self, value):
        return str(value)


class EnumField(StrField):
    def __init__(self, *, enum_=None, **kwargs):
        if isinstance(enum_, (list, tuple)):
            self._enum = tuple(str(x) for x in enum_)
        else:
            self._enum = enum_

        super().__init__(**kwargs)

    def get_value(self, value):
        value = super().get_value(value)
        if isinstance(self._enum, enum.EnumMeta):
            try:
                return self._enum[value]
            except KeyError:
                enums_str = ",".join(self._enum.__members__.keys())
                raise abort(
                    status=400,
                    text='Field {} enum ({})'.format(self.name, enums_str)
                )
        elif value in self._enum:
            return value
        else:
            raise abort(
                status=400,
                text='Field {} enum ({})'.format(self.name,
                                                 ",".join(self._enum))
            )
