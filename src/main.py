from fastapi import FastAPI
from router import user_router, admin_router
import uvicorn

from src.model.db_model import initialize_db

app = FastAPI()

app.include_router(user_router.router, prefix="/user", tags=["users"])
app.include_router(admin_router.router, prefix="/admin", tags=["Admin"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug")


@app.on_event("startup")
async def init_db():
    initialize_db()
