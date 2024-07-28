from pydantic import BaseModel, EmailStr
from typing import Optional, List

class EmailSchema(BaseModel):
    to: List[EmailStr]
    cc: Optional[List[EmailStr]] = None
    bcc: Optional[List[EmailStr]] = None
    subject: str
    body: str
    attachments: Optional[List[str]] = None