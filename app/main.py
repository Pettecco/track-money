from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.authentication._user import _User
from app.authentication.route import user_router
from app.infra.database import create_tables, init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    create_tables()
    yield


app = FastAPI(
    title="Track Money",
    description="A simple application to track your finances",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(user_router, prefix="/users")


@app.get("/health")
async def health_check():
    return JSONResponse({"status": "ok"})


def main() -> None:
    print("Hello from track-money")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
