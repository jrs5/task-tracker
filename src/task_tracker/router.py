from .fastapi_utils import LoggedRouter
from .ping import router as ping

TAG_SYSTEM = "System"


router = LoggedRouter()
router.include_router(ping.router, tags=[TAG_SYSTEM])
