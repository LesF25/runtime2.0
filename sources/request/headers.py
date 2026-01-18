from collections import UserDict
from functools import cached_property
from typing import Any

from request.cookies import VDOM_cookies


class VDOM_headers(UserDict[str, str]):
    def __init__(
        self,
        data: dict | None = None,
        **kwargs,
    ) -> None:
        super().__init__()
        self.update(data or {}, **kwargs)

    def __setitem__(
        self,
        key: str,
        value: Any,
    ) -> None:
        super().__setitem__(
            self._validate_key(key),
            self._validate_value(value),
        )

    def __getitem__(self, key: str) -> str:
        return super().__getitem__(
            self._validate_key(key),
        )

    def __contains__(self, key: str) -> bool:
        return super().__contains__(
            self._validate_key(key),
        )

    def get(self, key: str, default: Any = None) -> Any:
        return super().get(
            self._validate_key(key),
            default,
        )

    def pop(self, key: str, default: Any = None) -> str:
        return super().pop(
            self._validate_key(key),
            default,
        )

    def add(self, key: str, value: str) -> None:
        if key in self:
            self[key] = f'{self[key]}, {self._validate_value(value)}'
        else:
            self[key] = value

    def _validate_key(self, key: Any) -> str:
        if not isinstance(key, str):
            raise TypeError(f'Header name must be a string, not {type(key).__name__}')

        return key.lower()

    def _validate_value(self, value: Any) -> str:
        if not isinstance(
            value,
            self._valid_value_types,
        ):
            raise TypeError(f'Header value must be str, int, or float, not {type(value).__name__}')

        return str(value)

    @cached_property
    def _valid_value_types(self) -> tuple:
        return (
            str, int, float,
            VDOM_cookies,
        )
