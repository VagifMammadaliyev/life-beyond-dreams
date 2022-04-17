from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.exceptions import APIError
from api.urls import router

app = FastAPI()
app.include_router(router)


@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    error_response_body = {"detail": exc.detail}
    if exc.error_data:
        error_response_body["error"] = exc.error_data
    return JSONResponse(content=error_response_body, status_code=exc.status_code)
