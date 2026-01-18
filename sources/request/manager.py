import threading

from sources.request import VDOM_request
from sources.utils.exception import VDOM_exception


class VDOM_request_manager:
	def __init__(self) -> None:
		self._local = threading.local()

	@property
	def current(self) -> VDOM_request:
		request: VDOM_request = getattr(self._local, 'current_request')
		if request is None:
			raise VDOM_exception(
				'No request associated with current thread'
			)

		return request

	@current.setter
	def current(self, request: VDOM_request) -> None:
		self._local.current_request = request

	@current.deleter
	def current(self) -> None:
		if hasattr(self._local, 'current_request'):
			del self._local.current_request

	def __getitem__(self, key) -> None: raise AttributeError
	def __setitem__(self, key, value) -> None: raise AttributeError
	def __delitem__(self, key) -> None: raise AttributeError
	def __contains__(self, key) -> None: raise AttributeError
