import time
from fastapi import FastAPI, Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable, Awaitable

class RateLimitMiddleware(BaseHTTPMiddleware):
    
    def __init__(self, app: FastAPI, max_requests: int, window_seconds: int) -> None:
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:

        client_ip = request.client.host
        if client_ip not in self.requests:
            self.requests[client_ip] = []

        request_times = self.requests[client_ip]
        current_time = time.time()

        self.requests[client_ip] = [
            req_time for req_time in request_times if current_time - req_time < self.window_seconds
        ]

        if len(self.requests[client_ip]) >= self.max_requests:
            return Response('Too Many Requests', status_code=status.HTTP_429_TOO_MANY_REQUESTS)

        self.requests[client_ip].append(current_time)
        response = await call_next(request)
        return response


