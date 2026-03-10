from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api.base import router as base_router
from .api.user import router as user_router
from .api.category import router as category_router
from .api.location import router as location_router
from .api.post import router as post_router
from .api.comment import router as comment_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Blog API",
        description="API для блога",
        version="1.0.0",
        root_path="/api/v1"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(base_router)
    app.include_router(user_router)
    app.include_router(category_router)
    app.include_router(location_router)
    app.include_router(post_router)
    app.include_router(comment_router)

    return app