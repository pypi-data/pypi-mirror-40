from .client import BaseClient
from .utils import import_string


class Session:

    HEADER_PRIVATE_TOKEN = 'Private-Token'

    client_package = 'gitlab_caller.client'

    def __init__(self, base_url: str, private_token=None, **kwargs):
        self._base_url = base_url
        self._private_token = private_token

    def client(self, name: str) -> BaseClient:
        name = name.capitalize() + 'Client'
        cls = import_string(self.client_package + '.' + name)
        if issubclass(cls, BaseClient):
            return cls(session=self, name=name)
        raise ValueError('invalid class type {}'.format(cls))

    @property
    def base_url(self):
        return self._base_url

    @property
    def private_token(self):
        return self._private_token
