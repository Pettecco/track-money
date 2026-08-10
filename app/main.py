import logging

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.authentication.route import user_router
from app.domain_exception import DomainException
from app.infra.database import create_tables, init_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
init_database()
create_tables()

app = FastAPI(
    title="Track Money",
    description="A simple application to track your finances",
    version="0.1.0",
)

app.include_router(user_router, prefix="/users")


@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    logger.warning(f"DomainException ocurred: {exc.message}")
    return JSONResponse(status_code=400, content={"detail": exc.message})


@app.get("/health")
async def health_check():
    return JSONResponse({"status": "ok"})


def main() -> None:
    print("Hello from track-money")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
