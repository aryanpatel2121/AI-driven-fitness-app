from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    gender: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    gender: Optional[str] = None

class UserResponse(UserBase):
    id: str
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Workout Schemas
class ExerciseBase(BaseModel):
    name: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None
    distance: Optional[float] = None

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseResponse(ExerciseBase):
    id: str
    workout_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class WorkoutBase(BaseModel):
    name: str
    workout_type: Optional[str] = None
    duration: Optional[int] = None
    calories_burned: Optional[float] = None
    notes: Optional[str] = None

class WorkoutCreate(WorkoutBase):
    log_date: Optional[datetime] = None
    exercises: List[ExerciseCreate] = []

class WorkoutResponse(WorkoutBase):
    id: str
    user_id: str
    log_date: datetime
    created_at: datetime
    exercises: List[ExerciseResponse] = []
    
    class Config:
        from_attributes = True

# Nutrition Schemas
class NutritionLogBase(BaseModel):
    meal_type: str
    food_name: str
    calories: float
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fats: Optional[float] = None
    serving_size: Optional[str] = None

class NutritionLogCreate(NutritionLogBase):
    log_date: Optional[datetime] = None

class NutritionLogResponse(NutritionLogBase):
    id: str
    user_id: str
    log_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# Goal Schemas
class GoalBase(BaseModel):
    goal_type: str
    target_value: float
    current_value: Optional[float] = None
    target_date: Optional[datetime] = None

class GoalCreate(GoalBase):
    pass

class GoalResponse(GoalBase):
    id: str
    user_id: str
    is_achieved: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
