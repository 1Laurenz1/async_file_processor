from fastapi import FastAPI
import uvicorn


def create_app():
    app = FastAPI(
        debug=True,
        description="File processing service with background workers using FastAPI and RabbitMQ"
    )
    
    # app.include_router(...)
    
    return app


if __name__ == '__main__':
    uvicorn.run(
        "app.main:create_app",
        factory=True,
        reload=True
    )