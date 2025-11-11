from fastapi import FastAPI
import uvicorn


def create_app():
    app = FastAPI(
        debug=True,
        description="Production-ready file processing service with background workers using FastAPI and RabbitMQ"
    )