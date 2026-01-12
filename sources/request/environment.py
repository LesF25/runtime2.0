import socket
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from sources.version import SERVER_NAME, SERVER_VERSION
from sources.web.wsgi_request_handler import VDOM_wsgi_request_handler


class VDOM_environment:
	def __init__(
		self,
		headers: dict[str, Any],
		handler: VDOM_wsgi_request_handler,
	) -> None:
		self.__environment = {
			f'HTTP_{key.upper()}': str(val)
			for key, val in headers.items()
		}

		self.__environment['REQUEST_METHOD'] = handler.command
		self.__environment['DOCUMENT_ROOT'] = str(Path.cwd())
		self.__environment['GATEWAY_INTERFACE'] = 'CGI/1.1'

		parsed_url = urlparse(handler.path)
		url_path = parsed_url.path

		self.__environment['REQUEST_URI'] = url_path
		self.__environment['QUERY_STRING'] = parsed_url.query

		if '..' in Path(url_path).parts:
			self.__environment['SCRIPT_NAME'] = '/'
		else:
			self.__environment['SCRIPT_NAME'] = url_path

		self.__environment['REMOTE_ADDR'] = str(handler.client_address[0])
		self.__environment['REMOTE_PORT'] = str(handler.client_address[1])

		server_ip = socket.gethostbyname(
			socket.gethostname()
		)
		self.__environment['SERVER_ADDR'] = server_ip

		http_host = self.__environment.get('HTTP_HOST', server_ip)
		self.__environment['HTTP_HOST'] = http_host.split(':')[0]
		self.__environment['SERVER_PORT'] = str(handler.server.server_address[1])

		self.__environment['SERVER_NAME'] = SERVER_NAME
		self.__environment['SERVER_VERSION'] = SERVER_VERSION
		self.__environment['SERVER_PROTOCOL'] = 'HTTP/1.1'
		self.__environment['SERVER_SOFTWARE'] = f'Python {sys.version_info.major}.{sys.version_info.minor}'

	@property
	def environment(self):
		return self.__environment
