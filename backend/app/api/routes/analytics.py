from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
import pandas as pd
from app.api.routes.auth import oauth2_scheme
from app.core.security import decode_access_token
from app.services.firestore_service import firestore_service

router = APIRouter()

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """Get current user ID from token"""
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    username = payload.get("sub")
    user = firestore_service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user["id"]

@router.get("/progress")
async def get_progress_analytics(
    days: int = 30,
    user_id: str = Depends(get_current_user_id)
):
    """Get workout and nutrition progress analytics using Pandas"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get workouts
    all_workouts = firestore_service.get_user_workouts(user_id, limit=1000)
    workouts = [w for w in all_workouts if w.get("created_at") and w["created_at"] >= start_date]
    
    # Get nutrition logs
    all_nutrition = firestore_service.get_user_nutrition_logs(user_id, limit=1000)
    nutrition_logs = [n for n in all_nutrition if n.get("created_at") and n["created_at"] >= start_date]
    
    # Convert to DataFrames for analysis
    if workouts:
        workout_df = pd.DataFrame([{
            'date': w["created_at"].date() if isinstance(w["created_at"], datetime) else w["created_at"],
            'duration': w.get("duration", 0) or 0,
            'calories_burned': w.get("calories_burned", 0) or 0,
            'workout_type': w.get("workout_type", "unknown")
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
            'date': n["created_at"].date() if isinstance(n["created_at"], datetime) else n["created_at"],
            'calories': n.get("calories", 0),
            'protein': n.get("protein", 0) or 0,
            'carbs': n.get("carbs", 0) or 0,
            'fats': n.get("fats", 0) or 0
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
    user_id: str = Depends(get_current_user_id)
):
    """Get trend analysis for specific metrics"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    if metric in ["calories_burned", "duration"]:
        # Workout metrics
        all_workouts = firestore_service.get_user_workouts(user_id, limit=1000)
        workouts = [w for w in all_workouts if w.get("created_at") and w["created_at"] >= start_date]
        
        if not workouts:
            return {"trend": "no_data", "data": []}
        
        df = pd.DataFrame([{
            'date': w["created_at"].date() if isinstance(w["created_at"], datetime) else w["created_at"],
            'value': w.get(metric, 0) or 0
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
    user_id: str = Depends(get_current_user_id)
):
    """Get overall user statistics"""
    user = firestore_service.get_user_by_id(user_id)
    
    # Get all workouts and nutrition logs
    all_workouts = firestore_service.get_user_workouts(user_id, limit=10000)
    all_nutrition = firestore_service.get_user_nutrition_logs(user_id, limit=10000)
    
    total_workouts = len(all_workouts)
    total_nutrition_logs = len(all_nutrition)
    
    # Last 7 days activity
    last_week = datetime.utcnow() - timedelta(days=7)
    recent_workouts = len([
        w for w in all_workouts 
        if w.get("created_at") and w["created_at"] >= last_week
    ])
    
    return {
        "user_info": {
            "username": user.get("username"),
            "member_since": user.get("created_at").date() if user.get("created_at") else None
        },
        "totals": {
            "workouts": total_workouts,
            "nutrition_logs": total_nutrition_logs
        },
        "recent_activity": {
            "workouts_last_7_days": recent_workouts
        }
    }
