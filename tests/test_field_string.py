import enum

import pytest

from aiovalidator import StrField, EnumField
from aiovalidator.middlewares.exception import HTTPExceptionJson


@pytest.mark.parametrize('val,resp', (
        (2, '2'), ('2', '2'), ('2.9', '2.9'), (None, 'None'), ([], '[]')
))
def test_field_int(val, resp):
    fdatetime = StrField()
    assert fdatetime.get_value(val) == resp


class MyEnum(enum.Enum):
    do = 'do test'
    foo = 'foo test'


@pytest.mark.parametrize('enum_,val,resp', (
        (('do', 'foo'), 'do', 'do'),
        (MyEnum, 'do', MyEnum.do),
))
def test_field_enum(enum_, val, resp):
    fdatetime = EnumField(enum_=enum_)
    assert fdatetime.get_value(val) == resp


@pytest.mark.parametrize('enum_,val', (
        (('do', 'foo'), 'doo'),
        (MyEnum, 'doo'),
))
def test_field_enum_error(enum_, val):
    fdatetime = EnumField(enum_=enum_)
    with pytest.raises(HTTPExceptionJson):
        fdatetime.get_value(val)
