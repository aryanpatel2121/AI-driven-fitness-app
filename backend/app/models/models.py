from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    age = Column(Integer)
    weight = Column(Float)  # in kg
    height = Column(Float)  # in cm
    gender = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    workouts = relationship("Workout", back_populates="user")
    nutrition_logs = relationship("NutritionLog", back_populates="user")
    goals = relationship("Goal", back_populates="user")

class Workout(Base):
    __tablename__ = "workouts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    workout_type = Column(String)  # cardio, strength, flexibility, etc.
    duration = Column(Integer)  # in minutes
    calories_burned = Column(Float)
    notes = Column(String)
    log_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="workouts")
    exercises = relationship("Exercise", back_populates="workout")

class Exercise(Base):
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    name = Column(String, nullable=False)
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float)  # in kg
    distance = Column(Float)  # in km for cardio
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workout = relationship("Workout", back_populates="exercises")

class NutritionLog(Base):
    __tablename__ = "nutrition_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    meal_type = Column(String)  # breakfast, lunch, dinner, snack
    food_name = Column(String, nullable=False)
    calories = Column(Float)
    protein = Column(Float)  # in grams
    carbs = Column(Float)  # in grams
    fats = Column(Float)  # in grams
    serving_size = Column(String)
    log_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="nutrition_logs")

class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    goal_type = Column(String)  # weight_loss, muscle_gain, endurance, etc.
    target_value = Column(Float)
    current_value = Column(Float)
    target_date = Column(DateTime)
    is_achieved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="goals")
