import dataclasses

from sources import managers
from sources.request.environment import VDOM_environment
from sources.request.headers import VDOM_headers as VDOM_headers_
from sources.request.arguments import VDOM_request_arguments
from sources.utils.file_argument import File_argument, Attachment


@dataclasses.dataclass
class VDOM_arguments:
    arguments: VDOM_request_arguments

    def __getitem__(self, name):
        value = self.arguments[name]

        if (
            isinstance(value, list)
            and value
        ):
            return self.__try_decode(value[0])

        raise TypeError

    def __iter__(self):
        return iter(self.arguments)

    def keys(self):
        return list(self.arguments.keys())

    def get(self, name, default=None, castto=None):
        if (value := self.arguments.get(name)) is None:
            return default

        if not (
            (
                isinstance(value, list)
                and value
            )
            or isinstance(value, File_argument)
        ):
            return default

        if castto is list:
            return [self.__try_decode(item) for item in value]

        if castto is Attachment:
            if isinstance(value, File_argument):
                return Attachment(value)
            return default

        if isinstance(value, File_argument):
            return default

        item = self.__try_decode(value[0])
        return castto(item) if castto and item else item

    def __try_decode(self, item):
        if isinstance(item, bytes):
            return bytes(item).decode('utf-8', 'ignore')
        return item


@dataclasses.dataclass
class VDOM_headers:
    headers: VDOM_headers_
    headers_out: VDOM_headers_

    def __getitem__(self, name):
        return self.headers[name]

    def get(self, name, default = None):
        return self.headers.get(name, default)

    def keys(self) -> list[str]:
        return list(self.headers.keys())

    def __contains__(self, name):
        return name in self.headers_out

    def __iter__(self):
        return iter(self.headers_out)


@dataclasses.dataclass
class VDOM_client_information:
    environment: VDOM_environment

    @property
    def host(self) -> str:
        return self.environment.remote_addr

    @property
    def address(self) -> str:
        return self.environment.remote_addr

    @property
    def port(self) -> int:
        return int(self.environment.remote_port)


@dataclasses.dataclass
class VDOM_server_information:
    environment: VDOM_environment

    @property
    def host(self) -> str:
        return self.environment.http_host

    @property
    def address(self) -> str:
        return self.environment.server_addr

    @property
    def port(self) -> int:
        return int(self.environment.server_port)


@dataclasses.dataclass
class VDOM_protocol_information:
    environment: VDOM_environment

    @property
    def name(self) -> str:
        return self.environment.server_protocol.split('/')[0]

    @property
    def version(self) -> str:
        return self.environment.server_protocol.split('/')[1]


class VDOM_request:
    def __init__(self) -> None:
        request = managers.request_manager.current

        env = request.environment
        self.client = VDOM_client_information(env)
        self.server = VDOM_server_information(env)
        self.protocol = VDOM_protocol_information(env)

        self.headers = VDOM_headers(
            headers=request.headers,
            headers_out=request.headers_out,
        )

        self.arguments = VDOM_arguments(request.arguments)
        self.shared_vars = request.shared_variables

    def clear_files(self):
        files = managers.session_manager.current.files
        for x in files:
            files[x].remove()
        managers.session_manager.current.files = {}

    def uploaded_file(self, guid):
        u_file = managers.session_manager.current.files.pop(guid, None)
        return Attachment(u_file) if u_file else None

    @property
    def environment(self):
        return managers.request_manager.current.environment

    @property
    def cookies(self):
        return managers.request_manager.current.cookies

    @property
    def container(self):  # TODO: change stub to real container object
        class container_stub:
            def __init__(self):
                self.id = managers.request_manager.current.container_id
        return container_stub()

    @property
    def render_type(self):
        return managers.request_manager.current.render_type

    @property
    def dyn_libraries(self):
        return managers.request_manager.current.dyn_libraries
