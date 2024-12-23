
from fastapi import  HTTPException

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from core.security import verify_access_token


class OAuth2Middleware(BaseHTTPMiddleware):
    def __init__(self,app,excluded_routes):
        super().__init__(app)
        self.excluded_routes = excluded_routes

    async def dispatch(self, request: Request, call_next):

        if request.url.path not in self.excluded_routes:

            try:
                verify_access_token(request)

                response = await call_next(request)
                return response
            except HTTPException as exc:

                return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
            except Exception as exc:
                return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)
        else:
            response = await call_next(request)
            return response