from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.profile import ProfileUpdate, PasswordChange, UserResponse
from app.core.security import verify_password, get_password_hash
from app.core.auth import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/", response_model=UserResponse)
def read_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/", response_model=UserResponse)
def update_profile(
    data: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_user = db.query(User).filter(
        (User.email == data.email) | (User.username == data.username),
        User.id != current_user.id
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already in use."
        )

    current_user.username = data.username
    current_user.email = data.email
    db.commit()
    db.refresh(current_user)
    return current_user

@router.put("/password", status_code=status.HTTP_200_OK)
def change_password(
    data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password."
        )
    
    current_user.hashed_password = get_password_hash(data.new_password)
    db.commit()
    return {"message": "Password successfully updated"}