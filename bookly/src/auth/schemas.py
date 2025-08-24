from pydantic import BaseModel, Field, EmailStr
import uuid
from datetime import datetime


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length= 25)
    last_name: str = Field(max_length= 25)
    username: str = Field(min_length= 4, max_length= 16) 
    email: str = Field(max_length=40)
    password: str = Field(min_length= 8) 


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool 
    password_hash: str = Field(exclude= True)
    created_at: datetime 
    updated_at: datetime 
