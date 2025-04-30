from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.auth_router import router as auth_router
from api.v1.app_router import router as app_router
from api.v1.posts_router import router as post_router
from api.v1.subscriptions_router import router as sub_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(app_router, prefix="/api/v1")
app.include_router(post_router, prefix="/api/v1")
app.include_router(sub_router, prefix="/api/v1")



