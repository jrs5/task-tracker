from task_tracker.fastapi_utils import LoggedRouter

router = LoggedRouter()


@router.get("/ping")
def ping() -> str:
    return "pong"
