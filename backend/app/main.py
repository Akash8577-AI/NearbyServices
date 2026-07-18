from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.db.mongodb import client, db
from app.api.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ MongoDB Connected")
    yield
    client.close()
    print("❌ MongoDB Disconnected")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Include routers AFTER app is created
app.include_router(auth_router)


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
        return {
            "status": "success",
            "message": "MongoDB Connected Successfully"
        }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }