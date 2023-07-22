from pydantic import BaseModel
from pydantic import EmailStr


class User(BaseModel):
    name: str
    email: EmailStr
    phone: str
