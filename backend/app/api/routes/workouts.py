from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime
from app.schemas.schemas import WorkoutCreate, WorkoutResponse
from app.api.routes.auth import oauth2_scheme
from app.core.security import decode_access_token
from app.services.firestore_service import firestore_service

router = APIRouter()

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """Get current user ID from token"""
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    username = payload.get("sub")
    user = firestore_service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user["id"]

@router.post("", response_model=WorkoutResponse, status_code=status.HTTP_201_CREATED)
async def create_workout(
    workout: WorkoutCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Create a new workout"""
    workout_data = {
        "name": workout.name,
        "workout_type": workout.workout_type,
        "duration": workout.duration,
        "calories_burned": workout.calories_burned,
        "notes": workout.notes,
        "log_date": workout.log_date or datetime.utcnow()
    }
    
    workout_id = firestore_service.create_workout(user_id, workout_data)
    
    # Add exercises
    if workout.exercises:
        for exercise in workout.exercises:
            exercise_data = {
                "name": exercise.name,
                "sets": exercise.sets,
                "reps": exercise.reps,
                "weight": exercise.weight,
                "distance": exercise.distance
            }
            firestore_service.create_exercise(user_id, workout_id, exercise_data)
    
    # Get the created workout with exercises
    created_workout = firestore_service.get_workout_by_id(user_id, workout_id)
    created_workout["exercises"] = firestore_service.get_workout_exercises(user_id, workout_id)
    
    return created_workout

@router.get("", response_model=List[WorkoutResponse])
async def get_workouts(
    skip: int = 0,
    limit: int = 100,
    user_id: str = Depends(get_current_user_id)
):
    """Get all workouts for current user"""
    workouts = firestore_service.get_user_workouts(user_id, limit=limit)
    
    # Add exercises to each workout
    for workout in workouts:
        workout["exercises"] = firestore_service.get_workout_exercises(user_id, workout["id"])
    
    # Apply skip if needed (Firestore returns from start, we slice in Python)
    if skip > 0:
        workouts = workouts[skip:]
    
    return workouts

@router.get("/{workout_id}", response_model=WorkoutResponse)
async def get_workout(
    workout_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get a specific workout"""
    workout = firestore_service.get_workout_by_id(user_id, workout_id)
    
    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    
    # Add exercises
    workout["exercises"] = firestore_service.get_workout_exercises(user_id, workout_id)
    
    return workout

@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout(
    workout_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Delete a workout"""
    workout = firestore_service.get_workout_by_id(user_id, workout_id)
    
    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    
    firestore_service.delete_workout(user_id, workout_id)
    
    return None
