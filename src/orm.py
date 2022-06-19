from tortoise import Tortoise

from .models import Host, Session, SessionItem  # noqa

try:
    from .config import DB_USER
except ImportError:
    DB_USER = "waybackarchiver"

try:
    from .config import DB_PASSWORD
except ImportError:
    DB_PASSWORD = "waybackarchiver"

try:
    from .config import DB_NAME
except ImportError:
    DB_NAME = "waybackarchiver"

try:
    from .config import DB_HOST
except ImportError:
    DB_HOST = "localhost"

try:
    from .config import DB_PORT
except ImportError:
    DB_PORT = 5432


TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "user": DB_USER,
                "password": DB_PASSWORD,
                "database": DB_NAME,
                "host": DB_HOST,
                "port": DB_PORT,
            },
        },
    },
    "apps": {
        "models": {
            "models": [__name__, "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
    "maxsize": 20,
}


async def init():
    """Initialize the ORM."""
    await Tortoise.init(TORTOISE_ORM)
