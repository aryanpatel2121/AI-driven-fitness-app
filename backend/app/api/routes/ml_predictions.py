from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
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

@router.get("/predict-performance")
async def predict_workout_performance(
    workout_type: str = "strength",
    days_ahead: int = 7,
    user_id: str = Depends(get_current_user_id)
):
    """Predict future workout performance using Linear Regression"""
    # Get historical workout data
    all_workouts = firestore_service.get_user_workouts(user_id, limit=1000)
    workouts = [
        w for w in all_workouts 
        if w.get("workout_type") == workout_type
    ]
    workouts.sort(key=lambda x: x.get("created_at", datetime.min))
    
    if len(workouts) < 5:
        return {
            "error": "Insufficient data for prediction",
            "message": "Need at least 5 workouts of this type",
            "current_count": len(workouts)
        }
    
    # Prepare data
    df = pd.DataFrame([{
        'date': w["created_at"],
        'duration': w.get("duration", 0) or 0,
        'calories_burned': w.get("calories_burned", 0) or 0
    } for w in workouts])
    
    # Create day numbers for regression
    df['day_num'] = (df['date'] - df['date'].min()).dt.days
    
    # Train model for duration prediction
    X = df[['day_num']].values
    y_duration = df['duration'].values
    y_calories = df['calories_burned'].values
    
    # Duration model
    duration_model = LinearRegression()
    duration_model.fit(X, y_duration)
    
    # Calories model
    calories_model = LinearRegression()
    calories_model.fit(X, y_calories)
    
    # Make predictions
    last_day = df['day_num'].max()
    future_days = np.array([[last_day + i] for i in range(1, days_ahead + 1)])
    
    predicted_duration = duration_model.predict(future_days)
    predicted_calories = calories_model.predict(future_days)
    
    predictions = []
    for i, (dur, cal) in enumerate(zip(predicted_duration, predicted_calories)):
        predictions.append({
            "day": i + 1,
            "predicted_duration": max(0, round(float(dur), 2)),
            "predicted_calories": max(0, round(float(cal), 2))
        })
    
    return {
        "workout_type": workout_type,
        "historical_workouts": len(workouts),
        "predictions": predictions,
        "model_info": {
            "duration_score": round(duration_model.score(X, y_duration), 3),
            "calories_score": round(calories_model.score(X, y_calories), 3)
        }
    }

@router.get("/recommend-goals")
async def recommend_goals(
    user_id: str = Depends(get_current_user_id)
):
    """Recommend fitness goals based on user's historical data"""
    user = firestore_service.get_user_by_id(user_id)
    
    # Get last 30 days of workouts
    start_date = datetime.utcnow() - timedelta(days=30)
    all_workouts = firestore_service.get_user_workouts(user_id, limit=1000)
    workouts = [w for w in all_workouts if w.get("created_at") and w["created_at"] >= start_date]
    
    if not workouts:
        return {
            "message": "No recent workout data available",
            "recommendations": []
        }
    
    df = pd.DataFrame([{
        'duration': w.get("duration", 0) or 0,
        'calories_burned': w.get("calories_burned", 0) or 0,
        'workout_type': w.get("workout_type", "unknown")
    } for w in workouts])
    
    # Calculate statistics
    avg_duration = df['duration'].mean()
    avg_calories = df['calories_burned'].mean()
    workout_frequency = len(workouts) / 30  # workouts per day
    
    recommendations = []
    
    # Duration goal
    if avg_duration > 0:
        target_duration = avg_duration * 1.2  # 20% increase
        recommendations.append({
            "goal_type": "duration",
            "current_average": round(avg_duration, 2),
            "recommended_target": round(target_duration, 2),
            "unit": "minutes",
            "rationale": "Increase workout duration by 20%"
        })
    
    # Calorie burn goal
    if avg_calories > 0:
        target_calories = avg_calories * 1.15  # 15% increase
        recommendations.append({
            "goal_type": "calories_burned",
            "current_average": round(avg_calories, 2),
            "recommended_target": round(target_calories, 2),
            "unit": "calories",
            "rationale": "Increase calorie burn by 15%"
        })
    
    # Frequency goal
    if workout_frequency < 1:
        recommendations.append({
            "goal_type": "frequency",
            "current_average": round(workout_frequency * 7, 2),
            "recommended_target": 5,
            "unit": "workouts per week",
            "rationale": "Aim for 5 workouts per week"
        })
    
    return {
        "period_analyzed": "Last 30 days",
        "total_workouts": len(workouts),
        "recommendations": recommendations
    }

@router.get("/workout-insights")
async def get_workout_insights(
    user_id: str = Depends(get_current_user_id)
):
    """Get ML-powered insights about workout patterns"""
    workouts = firestore_service.get_user_workouts(user_id, limit=10000)
    
    if len(workouts) < 3:
        return {"message": "Need more workout data for insights"}
    
    df = pd.DataFrame([{
        'date': w["created_at"],
        'duration': w.get("duration", 0) or 0,
        'calories': w.get("calories_burned", 0) or 0,
        'type': w.get("workout_type", "unknown"),
        'day_of_week': w["created_at"].strftime('%A') if isinstance(w["created_at"], datetime) else "Unknown"
    } for w in workouts])
    
    insights = []
    
    # Best day of week
    if len(df) > 7:
        day_stats = df.groupby('day_of_week')['calories'].mean()
        best_day = day_stats.idxmax()
        insights.append({
            "type": "best_day",
            "message": f"You perform best on {best_day}s",
            "data": {"day": best_day, "avg_calories": round(day_stats.max(), 2)}
        })
    
    # Most common workout type
    if 'type' in df.columns:
        most_common = df['type'].mode()[0] if len(df['type'].mode()) > 0 else None
        if most_common:
            insights.append({
                "type": "preferred_workout",
                "message": f"Your most common workout type is {most_common}",
                "data": {"workout_type": most_common}
            })
    
    # Consistency score
    if len(df) > 14:
        last_14_days = datetime.utcnow() - timedelta(days=14)
        recent_workouts = df[df['date'] >= last_14_days]
        consistency = (len(recent_workouts) / 14) * 100
        
        insights.append({
            "type": "consistency",
            "message": f"Your workout consistency is {round(consistency, 1)}%",
            "data": {"consistency_score": round(consistency, 2)}
        })
    
    return {"insights": insights}
