from __future__ import annotations

from typing import ContextManager
import requests

from starwars.starwars_explorer.models.exceptions import ResourceDoesNotExist


class ApiClient(ContextManager):
    def __init__(self):
        self._session = None

    @property
    def session(self):
        assert self._session is not None
        return self._session

    def __enter__(self) -> ApiClient:
        assert self._session is None
        self._session = requests.session()
        return self

    def __exit__(self, exc_type, exc_val, traceback) -> None:
        self.session.close()
        self._session = None

    def get(self, url: str, **kwargs) -> dict:
        response = self.session.get(url, **kwargs)
        if response.status_code != 200:
            raise ResourceDoesNotExist('Resource does not exist')
        return response.json()
