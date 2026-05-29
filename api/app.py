from http import HTTPStatus

from fastapi import FastAPI

from .schemas.message import HealthStatus, Message

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    """Comentários da API"""
    return {"message": "Olá mundo!"}


@app.get("/health", status_code=HTTPStatus.OK, response_model=HealthStatus)
def health():
    return {"status": "ok"}
