from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Workout, Exercise, User
from app.schemas.schemas import WorkoutCreate, WorkoutResponse
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

@router.post("", response_model=WorkoutResponse, status_code=status.HTTP_201_CREATED)
async def create_workout(
    workout: WorkoutCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Create a new workout"""
    db_workout = Workout(
        user_id=user_id,
        name=workout.name,
        workout_type=workout.workout_type,
        duration=workout.duration,
        calories_burned=workout.calories_burned,
        notes=workout.notes,
        log_date=workout.log_date or datetime.utcnow()
    )
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    
    # Add exercises
    for exercise in workout.exercises:
        db_exercise = Exercise(
            workout_id=db_workout.id,
            name=exercise.name,
            sets=exercise.sets,
            reps=exercise.reps,
            weight=exercise.weight,
            distance=exercise.distance
        )
        db.add(db_exercise)
    
    db.commit()
    db.refresh(db_workout)
    
    return db_workout

@router.get("", response_model=List[WorkoutResponse])
async def get_workouts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Get all workouts for current user"""
    workouts = db.query(Workout).filter(Workout.user_id == user_id).order_by(Workout.log_date.desc()).offset(skip).limit(limit).all()
    return workouts

@router.get("/{workout_id}", response_model=WorkoutResponse)
async def get_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Get a specific workout"""
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == user_id
    ).first()
    
    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    
    return workout

@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Delete a workout"""
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == user_id
    ).first()
    
    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    
    db.delete(workout)
    db.commit()
    
    return None
