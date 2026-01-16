import hashlib
from dataclasses import dataclass, field


@dataclass(slots=True)
class VDOM_user:
    """User class defines behaviour of account"""

    id: str = ''
    login: str = ''
    password: str = ''
    first_name: str = ''
    last_name: str = ''
    email: str = ''
    security_level: str = ''
    system: bool = False

    member_of: list[str] = field(
		default_factory=list
	)

    def get_password_hash(self) -> str:
        return hashlib.md5(self.password.encode()).hexdigest()
