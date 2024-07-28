from pydantic import BaseModel, EmailStr, conint, constr
from typing import Optional, Literal

class CreateUser(BaseModel):
    username: constr(strip_whitespace=True, min_length=1, max_length=100) # type: ignore
    first_name: constr(strip_whitespace=True, min_length=1, max_length=50) # type: ignore
    middle_name: Optional[constr(strip_whitespace=True, min_length=1, max_length=50)] = None # type: ignore
    last_name: constr(strip_whitespace=True, min_length=1, max_length=50) # type: ignore
    email: EmailStr

class UpdateUser(BaseModel):
    username: Optional[constr(strip_whitespace=True, min_length=1, max_length=100)] = None # type: ignore
    first_name: Optional[constr(strip_whitespace=True, min_length=1, max_length=50)] = None # type: ignore
    middle_name: Optional[constr(strip_whitespace=True, min_length=1, max_length=50)] = None # type: ignore
    last_name: Optional[constr(strip_whitespace=True, min_length=1, max_length=50)] = None # type: ignore
    email: Optional[EmailStr] = None
    gender: Optional[Literal['Male', 'Female']] = None 
    age: Optional[conint(ge=18)] = None # type: ignore
    bio: Optional[constr(strip_whitespace=True, min_length=1, max_length=320)] = None # type: ignore
    preferences: Optional[constr(strip_whitespace=True, min_length=1, max_length=320)] = None # type: ignore

