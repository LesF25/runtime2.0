import socket
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse

from sources.version import SERVER_NAME, SERVER_VERSION
from sources.web.wsgi_request_handler import VDOM_wsgi_request_handler


@dataclass
class VDOM_environment:
    request_method: str
    request_uri: str
    query_string: str
    script_name: str
    remote_addr: str
    remote_port: str
    server_addr: str
    server_port: str
    http_host: str

    # CONSTANTS
    document_root: str = field(default_factory=lambda: str(Path.cwd()))
    gateway_interface: str = 'CGI/1.1'
    server_name: str = SERVER_NAME
    server_version: str = SERVER_VERSION
    server_protocol: str = 'HTTP/1.1'
    server_software: str = f'Python {sys.version_info.major}.{sys.version_info.minor}'

    headers: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_request(
        cls,
        headers: dict[str, Any],
        handler: VDOM_wsgi_request_handler,
    ) -> 'VDOM_environment':
        parsed_url = urlparse(handler.path)
        url_path = parsed_url.path

        script_name = (
            '/'
            if '..' in Path(url_path).parts
            else url_path
        )

        server_ip = socket.gethostbyname(socket.gethostname())
        client_ip, client_port = handler.client_address

        http_host = headers.get('Host', server_ip).split(':')[0]

        http_headers = {
            f'HTTP_{key.upper()}': str(val)
            for key, val in headers.items()
        }

        return cls(
            request_method=handler.command,
            request_uri=url_path,
            query_string=parsed_url.query,
            script_name=script_name,
            remote_addr=client_ip,
            remote_port=client_port,
            server_addr=server_ip,
            server_port=handler.server.server_address[1],
            http_host=http_host,
            headers=http_headers,
        )
