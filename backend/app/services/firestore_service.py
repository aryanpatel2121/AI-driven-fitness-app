from datetime import datetime
from typing import Dict, List, Optional, Any
from google.cloud.firestore_v1 import FieldFilter
from app.core.firebase_config import get_db

# Collection names
USERS_COLLECTION = "users"
WORKOUTS_COLLECTION = "workouts"
EXERCISES_COLLECTION = "exercises"
NUTRITION_LOGS_COLLECTION = "nutrition_logs"
GOALS_COLLECTION = "goals"

class FirestoreService:
    """Service for interacting with Firestore database"""
    
    def __init__(self):
        self.db = get_db()
    
    # ============ USER OPERATIONS ============
    
    def create_user(self, user_data: Dict) -> str:
        """Create a new user document"""
        user_data['created_at'] = datetime.utcnow()
        user_data['is_active'] = True
        doc_ref = self.db.collection(USERS_COLLECTION).document()
        doc_ref.set(user_data)
        return doc_ref.id
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        users = self.db.collection(USERS_COLLECTION).where(
            filter=FieldFilter("email", "==", email)
        ).limit(1).stream()
        
        for user in users:
            user_data = user.to_dict()
            user_data['id'] = user.id
            return user_data
        return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        users = self.db.collection(USERS_COLLECTION).where(
            filter=FieldFilter("username", "==", username)
        ).limit(1).stream()
        
        for user in users:
            user_data = user.to_dict()
            user_data['id'] = user.id
            return user_data
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        doc = self.db.collection(USERS_COLLECTION).document(user_id).get()
        if doc.exists:
            user_data = doc.to_dict()
            user_data['id'] = doc.id
            return user_data
        return None
    
    def update_user(self, user_id: str, update_data: Dict) -> bool:
        """Update user document"""
        try:
            self.db.collection(USERS_COLLECTION).document(user_id).update(update_data)
            return True
        except Exception:
            return False
    
    # ============ WORKOUT OPERATIONS ============
    
    def create_workout(self, user_id: str, workout_data: Dict) -> str:
        """Create a new workout for a user"""
        workout_data['user_id'] = user_id
        workout_data['log_date'] = workout_data.get('log_date', datetime.utcnow())
        workout_data['created_at'] = datetime.utcnow()
        
        doc_ref = self.db.collection(USERS_COLLECTION).document(user_id)\
            .collection(WORKOUTS_COLLECTION).document()
        doc_ref.set(workout_data)
        return doc_ref.id
    
    def get_user_workouts(self, user_id: str, limit: int = 100) -> List[Dict]:
        """Get all workouts for a user"""
        workouts = self.db.collection(USERS_COLLECTION).document(user_id)\
            .collection(WORKOUTS_COLLECTION)\
            .order_by('log_date', direction='DESCENDING')\
            .limit(limit)\
            .stream()
        
        result = []
        for workout in workouts:
            workout_data = workout.to_dict()
            workout_data['id'] = workout.id
            result.append(workout_data)
        return result
    
    def get_workout_by_id(self, user_id: str, workout_id: str) -> Optional[Dict]:
        """Get a specific workout"""
        doc = self.db.collection(USERS_COLLECTION).document(user_id)\
            .collection(WORKOUTS_COLLECTION).document(workout_id).get()
        
        if doc.exists:
            workout_data = doc.to_dict()
            workout_data['id'] = doc.id
            return workout_data
        return None
    
    def update_workout(self, user_id: str, workout_id: str, update_data: Dict) -> bool:
        """Update a workout"""
        try:
            self.db.collection(USERS_COLLECTION).document(user_id)\
                .collection(WORKOUTS_COLLECTION).document(workout_id).update(update_data)
            return True
        except Exception:
            return False
    
    def delete_workout(self, user_id: str, workout_id: str) -> bool:
        """Delete a workout and its exercises"""
        try:
            # Delete all exercises first
            exercises = self.db.collection(USERS_COLLECTION).document(user_id)\
                .collection(WORKOUTS_COLLECTION).document(workout_id)\
                .collection(EXERCISES_COLLECTION).stream()
            
            for exercise in exercises:
                exercise.reference.delete()
            
            # Delete the workout
            self.db.collection(USERS_COLLECTION).document(user_id)\
                .collection(WORKOUTS_COLLECTION).document(workout_id).delete()
            return True
        except Exception:
            return False
    
    # ============ EXERCISE OPERATIONS ============
    
    def create_exercise(self, user_id: str, workout_id: str, exercise_data: Dict) -> str:
        """Create an exercise within a workout"""
        exercise_data['workout_id'] = workout_id
        exercise_data['created_at'] = datetime.utcnow()
        
        doc_ref = self.db.collection(USERS_COLLECTION).document(user_id)\
            .collection(WORKOUTS_COLLECTION).document(workout_id)\
            .collection(EXERCISES_COLLECTION).document()
        doc_ref.set(exercise_data)
        return doc_ref.id
    
    def get_workout_exercises(self, user_id: str, workout_id: str) -> List[Dict]:
        """Get all exercises for a workout"""
        exercises = self.db.collection(USERS_COLLECTION).document(user_id)\
            .collection(WORKOUTS_COLLECTION).document(workout_id)\
            .collection(EXERCISES_COLLECTION).stream()
        
        result = []
        for exercise in exercises:
            exercise_data = exercise.to_dict()
            exercise_data['id'] = exercise.id
            result.append(exercise_data)
        return result
    
    # ============ NUTRITION LOG OPERATIONS ============
    
    def create_nutrition_log(self, user_id: str, nutrition_data: Dict) -> str:
        """Create a nutrition log entry"""
        nutrition_data['user_id'] = user_id
        nutrition_data['log_date'] = nutrition_data.get('log_date', datetime.utcnow())
        nutrition_data['created_at'] = datetime.utcnow()
        
        doc_ref = self.db.collection(USERS_COLLECTION).document(user_id)\
            .collection(NUTRITION_LOGS_COLLECTION).document()
        doc_ref.set(nutrition_data)
        return doc_ref.id
    
    def get_user_nutrition_logs(self, user_id: str, limit: int = 100) -> List[Dict]:
        """Get nutrition logs for a user"""
        logs = self.db.collection(USERS_COLLECTION).document(user_id)\
            .collection(NUTRITION_LOGS_COLLECTION)\
            .order_by('log_date', direction='DESCENDING')\
            .limit(limit)\
            .stream()
        
        result = []
        for log in logs:
            log_data = log.to_dict()
            log_data['id'] = log.id
            result.append(log_data)
        return result
    
    def get_nutrition_log_by_id(self, user_id: str, log_id: str) -> Optional[Dict]:
        """Get a specific nutrition log"""
        doc = self.db.collection(USERS_COLLECTION).document(user_id)\
            .collection(NUTRITION_LOGS_COLLECTION).document(log_id).get()
        
        if doc.exists:
            log_data = doc.to_dict()
            log_data['id'] = doc.id
            return log_data
        return None
    
    def update_nutrition_log(self, user_id: str, log_id: str, update_data: Dict) -> bool:
        """Update a nutrition log"""
        try:
            self.db.collection(USERS_COLLECTION).document(user_id)\
                .collection(NUTRITION_LOGS_COLLECTION).document(log_id).update(update_data)
            return True
        except Exception:
            return False
    
    def delete_nutrition_log(self, user_id: str, log_id: str) -> bool:
        """Delete a nutrition log"""
        try:
            self.db.collection(USERS_COLLECTION).document(user_id)\
                .collection(NUTRITION_LOGS_COLLECTION).document(log_id).delete()
            return True
        except Exception:
            return False
    
    # ============ GOAL OPERATIONS ============
    
    def create_goal(self, user_id: str, goal_data: Dict) -> str:
        """Create a fitness goal"""
        goal_data['user_id'] = user_id
        goal_data['is_achieved'] = False
        goal_data['created_at'] = datetime.utcnow()
        
        doc_ref = self.db.collection(USERS_COLLECTION).document(user_id)\
            .collection(GOALS_COLLECTION).document()
        doc_ref.set(goal_data)
        return doc_ref.id
    
    def get_user_goals(self, user_id: str) -> List[Dict]:
        """Get all goals for a user"""
        goals = self.db.collection(USERS_COLLECTION).document(user_id)\
            .collection(GOALS_COLLECTION)\
            .order_by('created_at', direction='DESCENDING')\
            .stream()
        
        result = []
        for goal in goals:
            goal_data = goal.to_dict()
            goal_data['id'] = goal.id
            result.append(goal_data)
        return result
    
    def get_goal_by_id(self, user_id: str, goal_id: str) -> Optional[Dict]:
        """Get a specific goal"""
        doc = self.db.collection(USERS_COLLECTION).document(user_id)\
            .collection(GOALS_COLLECTION).document(goal_id).get()
        
        if doc.exists:
            goal_data = doc.to_dict()
            goal_data['id'] = doc.id
            return goal_data
        return None
    
    def update_goal(self, user_id: str, goal_id: str, update_data: Dict) -> bool:
        """Update a goal"""
        try:
            self.db.collection(USERS_COLLECTION).document(user_id)\
                .collection(GOALS_COLLECTION).document(goal_id).update(update_data)
            return True
        except Exception:
            return False
    
    def delete_goal(self, user_id: str, goal_id: str) -> bool:
        """Delete a goal"""
        try:
            self.db.collection(USERS_COLLECTION).document(user_id)\
                .collection(GOALS_COLLECTION).document(goal_id).delete()
            return True
        except Exception:
            return False

# Singleton instance
firestore_service = FirestoreService()
