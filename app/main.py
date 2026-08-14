import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.authentication import user_router
from app.domain_exception import DomainException
from app.infra.database import create_tables, init_database
from app.movement import movement_router
from app.subscription import subscription_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()
    await create_tables()
    yield


app = FastAPI(
    title="Track Money",
    description="A simple application to track your finances",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(user_router, prefix="/users")
app.include_router(subscription_router, prefix="/subscriptions")
app.include_router(movement_router, prefix="/movements")


@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    logger.warning(f"DomainException ocurred: {exc.message}")
    return JSONResponse(status_code=400, content={"detail": exc.message})


@app.get("/health")
async def health_check():
    return JSONResponse({"status": "ok"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
