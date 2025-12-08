from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import auth, nutrition, workouts, analytics, ml_predictions as ml, prediction

# Import SQLAlchemy models + engine
from app.core.database import Base, engine


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)


# -------------- CREATE ALL TABLES (IMPORTANT) -------------------
# This fixes: sqlite3.OperationalError: no such table: users
Base.metadata.create_all(bind=engine)
# ---------------------------------------------------------------


# ---- CORS ----
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# ---- Routes ----
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["auth"])
app.include_router(nutrition.router, prefix=f"{settings.API_V1_PREFIX}/nutrition", tags=["nutrition"])
app.include_router(workouts.router, prefix=f"{settings.API_V1_PREFIX}/workouts", tags=["workouts"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_PREFIX}/analytics", tags=["analytics"])
app.include_router(ml.router, prefix=f"{settings.API_V1_PREFIX}/ml", tags=["ml"])
app.include_router(prediction.router, prefix=f"{settings.API_V1_PREFIX}/prediction", tags=["prediction"])


@app.get("/")
async def root():
    return {
        "message": "Fitness Tracker API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
