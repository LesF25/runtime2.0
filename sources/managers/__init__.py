import sys
from threading import RLock
from typing import Any


class Managers:
    """Registry for lazy-loaded manager instances."""

    def __init__(self):
        self._lock = RLock()
        self._lazy_registry = {}

    def register(
        self,
        name: str,
        manager_class: type,
        lazy: bool = False,
    ) -> None:
        with self._lock:
            if lazy:
                self._lazy_registry[name] = manager_class
            else:
                setattr(self, name, manager_class())

    def has(self, *names: str) -> bool:
        return all(
            hasattr(self, name) or name in self._lazy_registry
            for name in names
        )

    def __getattr__(self, name: str) -> Any | None:
        with self._lock:
            if instance := self.__dict__.get(name):
                return instance

            if manager_class := self._lazy_registry.get(name):
                instance = manager_class()
                setattr(self, name, instance)
                return instance

            if name == '__spec__':
                return None

            raise AttributeError(name)


sys.modules[__name__] = Managers()

# anounce globals for further linting
if __name__ not in sys.modules:
    from logs import VDOM_log_manager as log
    from storage import VDOM_storage as storage
    from file_access import VDOM_file_manager as file_access
    from request import VDOM_request_manager as  request_manager
    from resource import VDOM_resource_manager as resource_manager
    from database import VDOM_database_manager as databse_manager
    from scripting import VDOM_compiler as compiler, VDOM_dispatcher as dispatcher
    from memory import VDOM_memory as memory
    from engine import VDOM_engine as engine    
    from server import VDOM_server as server
    # from mailing import VDOM_email_manager
    from session import VDOM_session_manager as session_manager
    from module import VDOM_module_manager as module_manager
    from soap import VDOM_soap_server as soap_server
    from webdav_server import VDOM_webdav_manager as webdav_manager

    #if not managers.has("server"): 
    if sys.version_info[0] < 3:
        import __builtin__ as builtins
    else:
        import builtins
    from startup.debug import debug, DebugFile
    builtins.debug = debug
    builtins.debugfile = DebugFile()
    builtins._ = lambda value: value
    VDOM_CONFIG_1 = {}
