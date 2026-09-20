from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import ingest, query, session
from config import API_TITLE, API_VERSION, ALLOWED_ORIGINS


def create_app() -> FastAPI:
    app = FastAPI(title=API_TITLE, version=API_VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(ingest.router)
    app.include_router(query.router)
    app.include_router(session.router)

    @app.get("/")
    async def root():
        return {"message": "running"}

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app


app = create_app()
