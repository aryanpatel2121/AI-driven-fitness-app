from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import pandas as pd
from app.core.database import get_db
from app.models.models import Workout, NutritionLog, User
from app.api.routes.auth import oauth2_scheme
from app.core.security import decode_access_token

router = APIRouter()

def get_current_user_id(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> int:
    """Get current user ID from token"""
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.id

@router.get("/progress")
async def get_progress_analytics(
    days: int = 30,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Get workout and nutrition progress analytics using Pandas"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get workouts
    workouts = db.query(Workout).filter(
        Workout.user_id == user_id,
        Workout.created_at >= start_date
    ).all()
    
    # Get nutrition logs
    nutrition_logs = db.query(NutritionLog).filter(
        NutritionLog.user_id == user_id,
        NutritionLog.created_at >= start_date
    ).all()
    
    # Convert to DataFrames for analysis
    if workouts:
        workout_df = pd.DataFrame([{
            'date': w.created_at.date(),
            'duration': w.duration or 0,
            'calories_burned': w.calories_burned or 0,
            'workout_type': w.workout_type
        } for w in workouts])
        
        # Group by date
        workout_summary = workout_df.groupby('date').agg({
            'duration': 'sum',
            'calories_burned': 'sum'
        }).reset_index()
        
        workout_data = workout_summary.to_dict('records')
        
        # Workout type distribution
        type_distribution = workout_df['workout_type'].value_counts().to_dict()
    else:
        workout_data = []
        type_distribution = {}
    
    if nutrition_logs:
        nutrition_df = pd.DataFrame([{
            'date': n.created_at.date(),
            'calories': n.calories,
            'protein': n.protein or 0,
            'carbs': n.carbs or 0,
            'fats': n.fats or 0
        } for n in nutrition_logs])
        
        # Group by date
        nutrition_summary = nutrition_df.groupby('date').agg({
            'calories': 'sum',
            'protein': 'sum',
            'carbs': 'sum',
            'fats': 'sum'
        }).reset_index()
        
        nutrition_data = nutrition_summary.to_dict('records')
        
        # Calculate averages
        avg_calories = nutrition_df['calories'].mean()
        avg_protein = nutrition_df['protein'].mean()
    else:
        nutrition_data = []
        avg_calories = 0
        avg_protein = 0
    
    return {
        "period_days": days,
        "workouts": {
            "total_count": len(workouts),
            "daily_data": workout_data,
            "type_distribution": type_distribution
        },
        "nutrition": {
            "daily_data": nutrition_data,
            "averages": {
                "calories": round(avg_calories, 2),
                "protein": round(avg_protein, 2)
            }
        }
    }

@router.get("/trends")
async def get_trends(
    metric: str = "calories_burned",
    days: int = 30,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Get trend analysis for specific metrics"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    if metric in ["calories_burned", "duration"]:
        # Workout metrics
        workouts = db.query(Workout).filter(
            Workout.user_id == user_id,
            Workout.created_at >= start_date
        ).all()
        
        if not workouts:
            return {"trend": "no_data", "data": []}
        
        df = pd.DataFrame([{
            'date': w.created_at.date(),
            'value': getattr(w, metric) or 0
        } for w in workouts])
        
        daily_data = df.groupby('date')['value'].sum().reset_index()
        
        # Calculate trend (simple linear regression)
        if len(daily_data) > 1:
            daily_data['day_num'] = range(len(daily_data))
            correlation = daily_data['day_num'].corr(daily_data['value'])
            trend = "increasing" if correlation > 0.1 else "decreasing" if correlation < -0.1 else "stable"
        else:
            trend = "insufficient_data"
        
        return {
            "metric": metric,
            "trend": trend,
            "data": daily_data[['date', 'value']].to_dict('records')
        }
    
    return {"error": "Invalid metric"}

@router.get("/statistics")
async def get_statistics(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Get overall user statistics"""
    user = db.query(User).filter(User.id == user_id).first()
    
    total_workouts = db.query(Workout).filter(Workout.user_id == user_id).count()
    total_nutrition_logs = db.query(NutritionLog).filter(NutritionLog.user_id == user_id).count()
    
    # Last 7 days activity
    last_week = datetime.utcnow() - timedelta(days=7)
    recent_workouts = db.query(Workout).filter(
        Workout.user_id == user_id,
        Workout.created_at >= last_week
    ).count()
    
    return {
        "user_info": {
            "username": user.username,
            "member_since": user.created_at.date()
        },
        "totals": {
            "workouts": total_workouts,
            "nutrition_logs": total_nutrition_logs
        },
        "recent_activity": {
            "workouts_last_7_days": recent_workouts
        }
    }
