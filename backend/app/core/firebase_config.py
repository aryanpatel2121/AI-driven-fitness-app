import firebase_admin
from firebase_admin import credentials, firestore
from app.core.config import settings
import os

# Initialize Firebase
_db = None

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    global _db
    
    if _db is not None:
        return _db
    
    try:
        # Priority 1: Check for JSON credentials in environment variable (Render deployment)
        firebase_creds_json = os.getenv('FIREBASE_CREDENTIALS_JSON')
        if firebase_creds_json:
            import json
            cred_dict = json.loads(firebase_creds_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            print("✓ Firebase initialized from FIREBASE_CREDENTIALS_JSON env var")
        # Priority 2: Check if credentials file path is provided
        elif hasattr(settings, 'FIREBASE_CREDENTIALS_PATH') and settings.FIREBASE_CREDENTIALS_PATH:
            cred_path = settings.FIREBASE_CREDENTIALS_PATH
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                print("✓ Firebase initialized from credentials file")
            else:
                raise FileNotFoundError(f"Firebase credentials file not found at: {cred_path}")
        # Priority 3: Use GOOGLE_APPLICATION_CREDENTIALS env var
        else:
            firebase_admin.initialize_app()
            print("✓ Firebase initialized with default credentials")
        
        _db = firestore.client()
        print("✓ Firebase Firestore client ready")
        return _db
    
    except Exception as e:
        print(f"✗ Error initializing Firebase: {e}")
        raise

def get_db():
    """Get Firestore database instance"""
    global _db
    if _db is None:
        _db = initialize_firebase()
    return _db

def close_firebase():
    """Close Firebase connection (cleanup)"""
    global _db
    if _db:
        # Firebase Admin SDK doesn't require explicit closing
        # but we can delete the app if needed
        try:
            firebase_admin.delete_app(firebase_admin.get_app())
            _db = None
        except Exception:
            pass
