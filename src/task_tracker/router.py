from .fastapi_utils import LoggedRouter
from .ping import router as ping
from .v1 import router as v1

TAG_SYSTEM = "System"


router = LoggedRouter()
router.include_router(ping.router, tags=[TAG_SYSTEM])
router.include_router(v1.router, prefix="/v1", tags=[TAG_SYSTEM])
