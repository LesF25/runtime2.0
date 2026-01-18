from collections import UserDict
from typing import Self


def parse_cookie_str(
	cookies: str,
) -> dict[str, str]:
	result = {}

	for item in cookies.split(';'):
		item = item.strip()
		if not item:
			continue

		if '=' not in item:
			continue

		key, val = item.split('=', 1)
		key = key.strip()
		if key:
			result[key] = val.strip()

	return result


class VDOM_cookies(UserDict[str, str]):
	@classmethod
	def from_str(cls, cookies: str | None) -> Self:
		if not cookies:
			return cls()

		return cls(parse_cookie_str(cookies))

	def __init__(
		self,
		data: dict | None = None,
	) -> None:
		super().__init__()
		self.update({
			str(key): str(val)
			for key, val in (data or {}).items()
		})

	def __str__(self) -> str:
		return '; '.join(
			f'{k}={v}'
			for k, v in self.data.items()
		)
