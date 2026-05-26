from fastapi import FastAPI

from starlette.middleware.sessions import SessionMiddleware

from routes.bale import router as bale_router
from routes.admin import router as admin_router

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="SUPER_SECRET_KEY"
)

app.include_router(bale_router)

app.include_router(admin_router)