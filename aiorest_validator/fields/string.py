import enum

from .base import BaseField

__all__ = ['StrField']


class StrField(BaseField):
    def get_value(self, value):
        return str(value)


class EnumField(StrField):
    def __init__(self, *, enum_=None, **kwargs):
        if isinstance(enum_, [list, tuple]):
            self._enum = tuple(str(x) for x in enum_)

        super().__init__(**kwargs)

    def get_value(self, value):
        value = super().get_value(value)
        if isinstance(self._enum, enum.Enum):
            return self._enum(value)