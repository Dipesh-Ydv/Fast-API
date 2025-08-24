from pydantic import BaseModel, Field, EmailStr


class UserCreateModel(BaseModel):
    username: str = Field(min_length= 4, max_length= 16) 
    email: str = Field(max_length=40)
    password: str = Field(min_length= 8)
