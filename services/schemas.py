from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, EmailStr, Field



class AccountCreateSchema(BaseModel):
    email: EmailStr
    password: str
    is_active: bool


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)
    is_active: Optional[bool] = None
    

class UserResponse(AccountCreateSchema):
    id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True