from typing import Any, Callable

from fastapi import APIRouter, Request, Response
from fastapi.routing import APIRoute

from task_tracker.logger import logger


class LoggerRouteHandler(APIRoute):
    """
    Handler for FastAPI with basic observability for AWS Lambda
    https://www.eliasbrange.dev/posts/observability-with-fastapi-aws-lambda-powertools/
    """

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def route_handler(request: Request) -> Response:
            # Add fastapi context to logs
            ctx = {
                "path": request.url.path,
                "route": self.path,
                "method": request.method,
            }
            logger.append_keys(fastapi=ctx)
            logger.info("Received request")

            return await original_route_handler(request)

        return route_handler


class LoggedRouter(APIRouter):
    """
    Wrapper for FastAPI APIRouter.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs, route_class=LoggerRouteHandler)
