from pydantic import BaseModel, EmailStr

class OTPRequest(BaseModel):
    username: str
    email: EmailStr

class OTPVerify(BaseModel):
    otp: int