from abc import ABC, abstractmethod

from aiohttp.hdrs import METH_ALL


class BaseField(ABC):
    def __init__(self, *, verbose_name: str = None, default: object = None,
                 required: bool = True, methods: set = None,
                 validator: object = None):
        """

        :param verbose_name: description field
        :param default: handler or data type
        :param required: If you specify a default value, forced to set false
        :param methods: HTTP methods
        :param validator: handler or data type
        """
        self.methods = set(str.upper(x)
                           for x in methods) if methods else METH_ALL
        self.verbose_name = verbose_name
        self.required = False if default is not None else required
        self._default = default
        self._validator = validator
        self._name = None

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """

        :param value:
        """
        self._name = value

    def default(self):
        if callable(self._default):
            return self._default()
        return self._default

    def _get_value(self, value):
        value = self.get_value(value)
        if callable(self._validator):
            return self._validator(value)

        return value

    @abstractmethod
    def get_value(self, value):
        raise NotImplemented('Not implemented validate')
