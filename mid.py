from services import AppLogger
from fastapi import Request

async def mid1(request: Request, call_next):
    log=AppLogger()
    log.info(f"{request.method} has started")
    response = await call_next(request)
    log.info(f"{request.method} has finished")
    return response
