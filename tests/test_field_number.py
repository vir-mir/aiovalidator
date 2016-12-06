import pytest

from aiovalidator import IntegerField, FloatField, BoolField
from aiovalidator.middlewares.exception import HTTPExceptionJson


@pytest.mark.parametrize('val', (2, '2', 2.9))
def test_field_int(val):
    fdatetime = IntegerField()
    assert fdatetime.get_value(val) == 2


@pytest.mark.parametrize('val', ('2.2', None, 'asdasd', '', []))
def test_field_int_error(val):
    fdatetime = IntegerField()
    with pytest.raises(HTTPExceptionJson):
        fdatetime.get_value(val)


@pytest.mark.parametrize('val', (2.0, '2.0', '2', 2))
def test_field_float(val):
    fdatetime = FloatField()
    assert fdatetime.get_value(val) == 2.0


@pytest.mark.parametrize('val', (None, 'asdasd', '', []))
def test_field_float_error(val):
    fdatetime = FloatField()
    with pytest.raises(HTTPExceptionJson):
        fdatetime.get_value(val)


@pytest.mark.parametrize('val', (True, 2, '2', '1.1', 2.9, 1))
def test_field_bool(val):
    fdatetime = BoolField()
    assert fdatetime.get_value(val) is True


@pytest.mark.parametrize('val', ('2.2', None, 'asdasd', '', []))
def test_field_bool_error(val):
    fdatetime = IntegerField()
    with pytest.raises(HTTPExceptionJson):
        fdatetime.get_value(val)
