# backend/app/main.py
import logging
import json
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import auth, nutrition, workouts, analytics, ml_predictions as ml, prediction
from app.core.firebase_config import initialize_firebase


# ----------------- Logging -----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"API_V1_PREFIX = {settings.API_V1_PREFIX!r}")
logger.info(f"RAW BACKEND_CORS_ORIGINS = {settings.BACKEND_CORS_ORIGINS!r}")


# --------------- FastAPI app ----------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)


# -------------- INITIALIZE FIREBASE -------------------
@app.on_event("startup")
async def startup_event():
    """Initialize Firebase on application startup"""
    try:
        initialize_firebase()
        logger.info("Firebase initialized successfully")
    except Exception as exc:
        logger.exception("Error initializing Firebase: %s", exc)
        raise
# -------------------------------------------------------


# ------------- CORS helpers & middleware --------------
def parse_origins(value) -> List[str]:
    """
    Accepts:
      - a Python list/tuple (already parsed)
      - a JSON array string: '["https://a","http://b"]'
      - a comma-separated string: "https://a, http://b"
    Returns a list of origin strings (possibly empty).
    """
    if not value:
        return []
    if isinstance(value, (list, tuple)):
        return [str(i) for i in value]
    s = str(value).strip()
    # try JSON first
    try:
        parsed = json.loads(s)
        if isinstance(parsed, (list, tuple)):
            return [str(i) for i in parsed]
    except Exception:
        pass
    # fallback to comma separated
    return [i.strip() for i in s.split(",") if i.strip()]


_origins = parse_origins(settings.BACKEND_CORS_ORIGINS)
logger.info(f"Raw BACKEND_CORS_ORIGINS from settings: {settings.BACKEND_CORS_ORIGINS!r}")
logger.info(f"Parsed CORS origins = {_origins!r}")

# CORS Middleware Configuration
if _origins:
    logger.info(f"Adding CORS middleware with origins: {_origins}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    logger.warning(
        "⚠️ No CORS origins configured (BACKEND_CORS_ORIGINS is empty). "
        "Temporarily allowing all origins for debugging. "
        "CONFIGURE BACKEND_CORS_ORIGINS in production!"
    )
    # Temporary: Allow all origins for debugging
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,  # Can't use credentials with allow_origins=["*"]
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


# Print mounted routes for debugging (check this in logs after startup)
for route in app.routes:
    try:
        route_path = getattr(route, "path", None)
        route_methods = getattr(route, "methods", None)
        logger.info(f"Route: path={route_path} methods={route_methods} name={route.name}")
    except Exception:
        logger.exception("Error printing route info for %r", route)


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
