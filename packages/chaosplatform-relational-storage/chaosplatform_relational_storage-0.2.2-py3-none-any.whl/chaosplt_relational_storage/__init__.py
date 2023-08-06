from .db import (  # noqa: W0611
    configure_storage, dispose_storage, get_storage, release_storage,
    RelationalStorage
)

__all__ = ["__version__", "configure_storage", "dispose_storage",
           "get_storage", "release_storage", "RelationalStorage"]
__version__ = '0.2.2'
