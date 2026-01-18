from collections import UserDict


class VDOM_cookies(UserDict[str, str]):
	def __init__(
		self,
		data: dict | None = None,
	) -> None:
		super().__init__()
		self.update(data or {})

	def __str__(self) -> str:
		return '; '.join(
			f'{k}={v}'
			for k, v in self.data.items()
		)
