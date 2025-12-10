from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime, timedelta
from app.schemas.schemas import NutritionLogCreate, NutritionLogResponse
from app.api.routes.auth import oauth2_scheme
from app.core.security import decode_access_token
from app.services.firestore_service import firestore_service

router = APIRouter()

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """Get current user ID from token"""
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid or expired token. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user = firestore_service.get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User account not found. Please register or log in again.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return user["id"]

@router.post("", response_model=NutritionLogResponse, status_code=status.HTTP_201_CREATED)
async def create_nutrition_log(
    nutrition: NutritionLogCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Create a new nutrition log entry"""
    nutrition_data = {
        "meal_type": nutrition.meal_type,
        "food_name": nutrition.food_name,
        "calories": nutrition.calories,
        "protein": nutrition.protein,
        "carbs": nutrition.carbs,
        "fats": nutrition.fats,
        "serving_size": nutrition.serving_size,
        "log_date": nutrition.log_date or datetime.utcnow()
    }
    
    log_id = firestore_service.create_nutrition_log(user_id, nutrition_data)
    created_log = firestore_service.get_nutrition_log_by_id(user_id, log_id)
    
    return created_log

@router.get("", response_model=List[NutritionLogResponse])
async def get_nutrition_logs(
    skip: int = 0,
    limit: int = 100,
    days: int = 7,
    user_id: str = Depends(get_current_user_id)
):
    """Get nutrition logs for current user (default: last 7 days)"""
    logs = firestore_service.get_user_nutrition_logs(user_id, limit=limit)
    
    # Filter by date range (last N days)
    start_date = datetime.utcnow() - timedelta(days=days)
    filtered_logs = [
        log for log in logs 
        if log.get("log_date") and log["log_date"] >= start_date
    ]
    
    # Apply skip if needed
    if skip > 0:
        filtered_logs = filtered_logs[skip:]
    
    return filtered_logs

@router.get("/daily-summary")
async def get_daily_summary(
    date: str = None,
    user_id: str = Depends(get_current_user_id)
):
    """Get daily nutrition summary"""
    if date:
        target_date = datetime.fromisoformat(date)
    else:
        target_date = datetime.utcnow()
    
    start_of_day = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    
    # Get all nutrition logs and filter by date
    all_logs = firestore_service.get_user_nutrition_logs(user_id, limit=1000)
    logs = [
        log for log in all_logs
        if log.get("log_date") and start_of_day <= log["log_date"] < end_of_day
    ]
    
    total_calories = sum(log.get("calories", 0) for log in logs)
    total_protein = sum(log.get("protein", 0) or 0 for log in logs)
    total_carbs = sum(log.get("carbs", 0) or 0 for log in logs)
    total_fats = sum(log.get("fats", 0) or 0 for log in logs)
    
    return {
        "date": target_date.date(),
        "total_calories": total_calories,
        "total_protein": total_protein,
        "total_carbs": total_carbs,
        "total_fats": total_fats,
        "meal_count": len(logs)
    }

@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_nutrition_log(
    log_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Delete a nutrition log"""
    log = firestore_service.get_nutrition_log_by_id(user_id, log_id)
    
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nutrition log not found")
    
    firestore_service.delete_nutrition_log(user_id, log_id)
    
    return None
