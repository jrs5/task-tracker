from task_tracker.fastapi_utils import LoggedRouter

from .tasks import router as tasks

TAG_SYSTEM = "System"


router = LoggedRouter()
router.include_router(tasks.router, prefix="/tasks", tags=[TAG_SYSTEM])
