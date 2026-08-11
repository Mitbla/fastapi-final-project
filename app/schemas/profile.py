from pydantic import BaseModel, ConfigDict, EmailStr, Field

class ProfileUpdate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)