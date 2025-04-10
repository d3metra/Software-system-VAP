from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from app import routers, errors

app = FastAPI(title="ares")

@app.exception_handler(errors.HTTPException)
async def http_execpion_handler(request: Request, exc: errors.HTTPException) -> Response:
    return JSONResponse(
        {"code": exc.code, "message": exc.message}, status_code=exc.status 
    )

app.include_router(routers.patents_router, prefix="/patents", tags=["Patents"])