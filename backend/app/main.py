from contextlib import asynccontextmanager
from app.api import category
from app.api import service
from app.api import provider
from app.api import booking

from fastapi import FastAPI

from app.core.config import settings
from app.db.mongodb import client, db
from app.api.auth import router as auth_router
from app.api import review




@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ MongoDB Connected")
    yield
    client.close()
    print("❌ MongoDB Disconnected")


app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, lifespan=lifespan)

# Include routers AFTER app is created
app.include_router(auth_router, prefix="/api/v1")
app.include_router(category.router, prefix="/api/v1")
app.include_router(service.router, prefix="/api/v1")
app.include_router(provider.router, prefix="/api/v1")
app.include_router(provider.router, prefix="/api/v1")
app.include_router(
    booking.router,
    prefix="/api/v1"
)
app.include_router(review.router, prefix="/api/v1")


@app.get("/")
async def home():
    return {"message": "Nearby Services API Running 🚀"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/db-check")
async def db_check():
    try:
        await db.command("ping")
        return {"status": "success", "message": "MongoDB Connected Successfully"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

    app.include_router(service.router, prefix="/api/v1")
