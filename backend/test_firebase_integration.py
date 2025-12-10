"""
Test script to verify Firebase integration
Run this after setting up Firebase credentials to ensure everything works
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from app.core.firebase_config import initialize_firebase, get_db
from app.services.firestore_service import firestore_service
from app.core.security import get_password_hash

def test_firebase_connection():
    """Test Firebase initialization"""
    print("=" * 60)
    print("TEST 1: Firebase Connection")
    print("=" * 60)
    try:
        db = initialize_firebase()
        print("✓ Firebase initialized successfully")
        print(f"✓ Firestore client: {db}")
        return True
    except Exception as e:
        print(f"✗ Firebase initialization failed: {e}")
        return False

def test_user_crud():
    """Test user CRUD operations"""
    print("\n" + "=" * 60)
    print("TEST 2: User CRUD Operations")
    print("=" * 60)
    
    test_email = f"test_{datetime.now().timestamp()}@example.com"
    test_username = f"testuser_{int(datetime.now().timestamp())}"
    
    try:
        # Create user
        print(f"Creating test user: {test_username}")
        user_data = {
            "email": test_email,
            "username": test_username,
            "hashed_password": get_password_hash("testpassword123"),
            "full_name": "Test User",
            "age": 25,
            "weight": 70.0,
            "height": 175.0,
            "gender": "male"
        }
        user_id = firestore_service.create_user(user_data)
        print(f"✓ User created with ID: {user_id}")
        
        # Retrieve user by email
        user = firestore_service.get_user_by_email(test_email)
        assert user is not None, "User not found by email"
        print(f"✓ User retrieved by email: {user['username']}")
        
        # Retrieve user by username
        user = firestore_service.get_user_by_username(test_username)
        assert user is not None, "User not found by username"
        print(f"✓ User retrieved by username: {user['email']}")
        
        # Update user
        update_success = firestore_service.update_user(user_id, {"age": 26})
        assert update_success, "User update failed"
        updated_user = firestore_service.get_user_by_id(user_id)
        assert updated_user["age"] == 26, "User age not updated"
        print(f"✓ User updated successfully: age changed to {updated_user['age']}")
        
        print(f"\n✓ All user CRUD tests passed!")
        return user_id
        
    except Exception as e:
        print(f"✗ User CRUD test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_workout_crud(user_id):
    """Test workout CRUD operations"""
    print("\n" + "=" * 60)
    print("TEST 3: Workout CRUD Operations")
    print("=" * 60)
    
    try:
        # Create workout
        print(f"Creating test workout for user: {user_id}")
        workout_data = {
            "name": "Morning Run",
            "workout_type": "cardio",
            "duration": 30,
            "calories_burned": 250.0,
            "notes": "Felt great!"
        }
        workout_id = firestore_service.create_workout(user_id, workout_data)
        print(f"✓ Workout created with ID: {workout_id}")
        
        # Create exercises
        exercise_data = {
            "name": "Running",
            "sets": None,
            "reps": None,
            "weight": None,
            "distance": 5.0
        }
        exercise_id = firestore_service.create_exercise(user_id, workout_id, exercise_data)
        print(f"✓ Exercise created with ID: {exercise_id}")
        
        # Retrieve workouts
        workouts = firestore_service.get_user_workouts(user_id)
        assert len(workouts) > 0, "No workouts found"
        print(f"✓ Retrieved {len(workouts)} workout(s)")
        
        # Retrieve exercises
        exercises = firestore_service.get_workout_exercises(user_id, workout_id)
        assert len(exercises) > 0, "No exercises found"
        print(f"✓ Retrieved {len(exercises)} exercise(s)")
        
        # Delete workout
        delete_success = firestore_service.delete_workout(user_id, workout_id)
        assert delete_success, "Workout deletion failed"
        print(f"✓ Workout deleted successfully")
        
        print(f"\n✓ All workout CRUD tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Workout CRUD test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_nutrition_crud(user_id):
    """Test nutrition log CRUD operations"""
    print("\n" + "=" * 60)
    print("TEST 4: Nutrition Log CRUD Operations")
    print("=" * 60)
    
    try:
        # Create nutrition log
        print(f"Creating test nutrition log for user: {user_id}")
        nutrition_data = {
            "meal_type": "breakfast",
            "food_name": "Oatmeal with berries",
            "calories": 350.0,
            "protein": 12.0,
            "carbs": 55.0,
            "fats": 8.0,
            "serving_size": "1 bowl"
        }
        log_id = firestore_service.create_nutrition_log(user_id, nutrition_data)
        print(f"✓ Nutrition log created with ID: {log_id}")
        
        # Retrieve nutrition logs
        logs = firestore_service.get_user_nutrition_logs(user_id)
        assert len(logs) > 0, "No nutrition logs found"
        print(f"✓ Retrieved {len(logs)} nutrition log(s)")
        
        # Delete nutrition log
        delete_success = firestore_service.delete_nutrition_log(user_id, log_id)
        assert delete_success, "Nutrition log deletion failed"
        print(f"✓ Nutrition log deleted successfully")
        
        print(f"\n✓ All nutrition CRUD tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Nutrition CRUD test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_persistence(test_user_id):
    """Test that data persists across queries"""
    print("\n" + "=" * 60)
    print("TEST 5: Data Persistence")
    print("=" * 60)
    
    try:
        # Retrieve user again
        user = firestore_service.get_user_by_id(test_user_id)
        assert user is not None, "User not found - data not persisting"
        print(f"✓ User data persists: {user['username']}")
        
        print(f"\n✓ Data persistence test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Data persistence test failed: {e}")
        return False

def cleanup_test_data(user_id):
    """Clean up test data"""
    print("\n" + "=" * 60)
    print("CLEANUP: Removing Test Data")
    print("=" * 60)
    
    try:
        # Note: In Firestore, we need to delete subcollections before deleting the user
        # For this test, we'll just note that the test user exists
        print(f"ℹ Test user {user_id} will remain in Firebase for manual inspection")
        print("You can delete it from Firebase Console if needed")
        return True
    except Exception as e:
        print(f"⚠ Cleanup warning: {e}")
        return False

def main():
    print("\n" + "=" * 60)
    print("FIREBASE INTEGRATION TEST SUITE")
    print("=" * 60)
    print("\nThis script will test:")
    print("1. Firebase connection")
    print("2. User CRUD operations")
    print("3. Workout CRUD operations")
    print("4. Nutrition log CRUD operations")
    print("5. Data persistence")
    print("\n" + "=" * 60)
    
    # Run tests
    test_results = []
    
    # Test 1: Firebase connection
    if not test_firebase_connection():
        print("\n❌ FATAL: Cannot connect to Firebase. Fix this before proceeding.")
        return
    test_results.append(True)
    
    # Test 2: User CRUD
    user_id = test_user_crud()
    if user_id:
        test_results.append(True)
    else:
        print("\n❌ User CRUD failed. Skipping remaining tests.")
        return
    
    # Test 3: Workout CRUD
    test_results.append(test_workout_crud(user_id))
    
    # Test 4: Nutrition CRUD
    test_results.append(test_nutrition_crud(user_id))
    
    # Test 5: Data persistence
    test_results.append(test_data_persistence(user_id))
    
    # Cleanup
    cleanup_test_data(user_id)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(test_results)
    total = len(test_results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED!")
        print("Firebase integration is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} TEST(S) FAILED")
        print("Please review the errors above.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
