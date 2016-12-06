import datetime
import time

import pytest

from aiovalidator import DateTimeField, DateField, TimeStampField
from aiovalidator.middlewares.exception import HTTPExceptionJson


@pytest.mark.parametrize('format_,date', (
        ('%Y-%m-%d %H:%M:%S', '2012-01-03 12:03:05'),
        ('%Y-%m-%d %H:%M', '2012-01-03 12:03'),
        ('%d.%m.%Y %H:%M:%S', '25.10.2016 12:03:05'),
))
def test_field_datetime(format_, date):
    fdatetime = DateTimeField(format_=format_)
    d = datetime.datetime.strptime(date, format_)
    assert fdatetime.get_value(date) == d


def test_field_datetime_error():
    fdatetime = DateTimeField()
    with pytest.raises(HTTPExceptionJson):
        fdatetime.get_value('asdasdasdas')


@pytest.mark.parametrize('format_,date', (
        ('%Y-%m-%d', '2012-01-03'),
        ('%d.%m.%Y', '25.10.2016'),
))
def test_field_date(format_, date):
    fdatetime = DateField(format_=format_)
    d = datetime.datetime.strptime(date, format_).date()
    assert fdatetime.get_value(date) == d


def test_field_date_error():
    fdatetime = DateField()
    with pytest.raises(HTTPExceptionJson):
        fdatetime.get_value('asdasdasdas')


def test_field_timestamp_error():
    fdatetime = TimeStampField()
    with pytest.raises(HTTPExceptionJson):
        fdatetime.get_value('asdasdasdas')


def test_field_timestamp():
    timestamp = int(time.time())
    fdatetime = TimeStampField()
    assert fdatetime.get_value(
        str(timestamp)) == datetime.datetime.fromtimestamp(timestamp)
