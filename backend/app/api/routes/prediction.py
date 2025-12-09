from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.services.ai_service import ai_service

router = APIRouter()

class NutritionPredictionRequest(BaseModel):
    query: str

class WorkoutPredictionRequest(BaseModel):
    activity: str
    duration: int

@router.post("/nutrition")
async def predict_nutrition(request: NutritionPredictionRequest):
    """Predict nutritional information for a food item"""
    try:
        result = await ai_service.predict_nutrition(request.query)
        return result
    except Exception as e:
        if "GOOGLE_API_KEY" in str(e):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Google API Key missing. Please add GOOGLE_API_KEY to backend/.env"
            )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/workout")
async def predict_workout(request: WorkoutPredictionRequest):
    """Predict calories burned for a workout"""
    try:
        result = await ai_service.predict_workout(request.activity, request.duration)
        return result
    except Exception as e:
        if "GOOGLE_API_KEY" in str(e):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Google API Key missing. Please add GOOGLE_API_KEY to backend/.env"
            )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
