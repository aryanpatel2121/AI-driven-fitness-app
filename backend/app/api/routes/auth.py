from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.security import verify_password, get_password_hash, create_access_token
from app.schemas.schemas import UserCreate, UserResponse, Token, UserUpdate
from app.core.config import settings
from app.services.firestore_service import firestore_service

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    """Register a new user"""
    # Check if user exists by email
    existing_user = firestore_service.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username is taken
    existing_user = firestore_service.get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    user_data = {
        "email": user.email,
        "username": user.username,
        "hashed_password": hashed_password,
        "full_name": user.full_name,
        "age": user.age,
        "weight": user.weight,
        "height": user.height,
        "gender": user.gender
    }
    
    user_id = firestore_service.create_user(user_data)
    
    # Get the created user to return
    created_user = firestore_service.get_user_by_id(user_id)
    
    return created_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login user and return access token"""
    user = firestore_service.get_user_by_username(form_data.username)
    
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current authenticated user"""
    from app.core.security import decode_access_token
    
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username: str = payload.get("sub")
    user = firestore_service.get_user_by_username(username)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    token: str = Depends(oauth2_scheme)
):
    """Update current authenticated user profile"""
    from app.core.security import decode_access_token
    
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username: str = payload.get("sub")
    user = firestore_service.get_user_by_username(username)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Prepare update data (only include non-None values)
    update_data = {}
    if user_update.full_name is not None:
        update_data["full_name"] = user_update.full_name
    if user_update.age is not None:
        update_data["age"] = user_update.age
    if user_update.weight is not None:
        update_data["weight"] = user_update.weight
    if user_update.height is not None:
        update_data["height"] = user_update.height
    if user_update.gender is not None:
        update_data["gender"] = user_update.gender
    
    # Update user in Firestore
    if update_data:
        firestore_service.update_user(user["id"], update_data)
    
    # Get updated user
    updated_user = firestore_service.get_user_by_id(user["id"])
    
    return updated_user
