
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response

logger = logging.getLogger("agromind")

SENSITIVE_HEADERS = {"authorization", "cookie", "set-cookie", "x-api-key", "x-device-token"}

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs method, path, status, processing time and masked headers.
    Add to FastAPI app with:
        app.add_middleware(RequestLoggingMiddleware)
    """
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        try:
            masked_headers = self._mask_headers(request.headers)
            logger.info(f"REQUEST START -> {request.method} {request.url.path} headers={masked_headers}")

            response: Response = await call_next(request)
            process_time = (time.time() - start) * 1000
            logger.info(f"REQUEST END   <- {request.method} {request.url.path} status={response.status_code} time_ms={process_time:.2f}")
            return response
        except Exception as exc:
            process_time = (time.time() - start) * 1000
            logger.exception(f"REQUEST ERROR  !! {request.method} {request.url.path} time_ms={process_time:.2f} error={exc}")
            raise

    def _mask_headers(self, headers):
        out = {}
        for k, v in headers.items():
            key = k.lower()
            if key in SENSITIVE_HEADERS:
                out[key] = "****"
            else:
                out[key] = v
        return out
