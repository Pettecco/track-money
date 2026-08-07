from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.authentication._user import _User

app = FastAPI(
    title="Track Money",
    description="A simple application to track your finances",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    user = _User(name="Test User", email="Teste@teste.com.br", password="12345678")
    return JSONResponse({"password": user.hashed_password})

    return JSONResponse({"status": "ok"})


def main() -> None:
    print("Hello from track-money")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
