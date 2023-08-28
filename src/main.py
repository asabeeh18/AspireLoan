import logging

import uvicorn
from fastapi import FastAPI
from starlette.requests import Request

from libs import error_handler
from model.db_model import initialize_db
from router import user_router, admin_router

app = FastAPI()

app.include_router(user_router.router, prefix="/user", tags=["users"])
app.include_router(admin_router.router, prefix="/admin", tags=["Admin"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug")


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    api = request.url.path
    logger.error(f' Error in API: {api}')
    return error_handler.create_error_response(request, exc)


def setup_logger():
    global logger
    logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)


@app.on_event("startup")
async def init_db():
    setup_logger()
    initialize_db()
