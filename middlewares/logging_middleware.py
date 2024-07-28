import time
import logging
import os
import uuid
from logging.handlers import RotatingFileHandler
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable, Awaitable

# log_file_path = os.path.join(os.getcwd(),'logs','middleware_logs','logging_middleware.log')
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         RotatingFileHandler(log_file_path, maxBytes=10485760, backupCount=3),
#         logging.StreamHandler() 
#     ]
# )
# logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        
        request_id = str(uuid.uuid1().hex)
        request.state.request_id = request_id

        # logger.info(f'Request ID: {request_id} - {request.method} {request.url}')
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        # logger.info(f'Request ID: {request_id} - Response: {response.status_code} (processed in {process_time:.4f} seconds)')

        return response