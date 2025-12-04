from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.models import NutritionLog, User
from app.schemas.schemas import NutritionLogCreate, NutritionLogResponse
from app.api.routes.auth import oauth2_scheme
from app.core.security import decode_access_token

router = APIRouter()

def get_current_user_id(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> int:
    """Get current user ID from token"""
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user.id

@router.post("", response_model=NutritionLogResponse, status_code=status.HTTP_201_CREATED)
async def create_nutrition_log(
    nutrition: NutritionLogCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Create a new nutrition log entry"""
    db_nutrition = NutritionLog(
        user_id=user_id,
        meal_type=nutrition.meal_type,
        food_name=nutrition.food_name,
        calories=nutrition.calories,
        protein=nutrition.protein,
        carbs=nutrition.carbs,
        fats=nutrition.fats,
        serving_size=nutrition.serving_size,
        log_date=nutrition.log_date or datetime.utcnow()
    )
    db.add(db_nutrition)
    db.commit()
    db.refresh(db_nutrition)
    
    return db_nutrition

@router.get("", response_model=List[NutritionLogResponse])
async def get_nutrition_logs(
    skip: int = 0,
    limit: int = 100,
    days: int = 7,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Get nutrition logs for current user (default: last 7 days)"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    logs = db.query(NutritionLog).filter(
        NutritionLog.user_id == user_id,
        NutritionLog.log_date >= start_date
    ).order_by(NutritionLog.log_date.desc()).offset(skip).limit(limit).all()
    
    return logs

@router.get("/daily-summary")
async def get_daily_summary(
    date: str = None,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Get daily nutrition summary"""
    if date:
        target_date = datetime.fromisoformat(date)
    else:
        target_date = datetime.utcnow()
    
    start_of_day = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    
    logs = db.query(NutritionLog).filter(
        NutritionLog.user_id == user_id,
        NutritionLog.log_date >= start_of_day,
        NutritionLog.log_date < end_of_day
    ).all()
    
    total_calories = sum(log.calories for log in logs)
    total_protein = sum(log.protein or 0 for log in logs)
    total_carbs = sum(log.carbs or 0 for log in logs)
    total_fats = sum(log.fats or 0 for log in logs)
    
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
    log_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Delete a nutrition log"""
    log = db.query(NutritionLog).filter(
        NutritionLog.id == log_id,
        NutritionLog.user_id == user_id
    ).first()
    
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nutrition log not found")
    
    db.delete(log)
    db.commit()
    
    return None
