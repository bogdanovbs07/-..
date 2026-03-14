from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ImageBase(BaseModel):
    filename: str
    description: Optional[str] = None

class ImageCreate(ImageBase):
    user_id: Optional[int] = None

class ImageResponse(ImageBase):
    id: int
    file_path: str
    created_at: datetime
    updated_at: datetime
    user_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
