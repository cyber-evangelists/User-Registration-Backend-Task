from beanie import Document
from pydantic import BaseModel, EmailStr
from typing import Optional
import re

# class User(Document):
#     cnic: str
#     forename: str
#     surname: str
#     address: str
#     email: str
#     password: Optional[str] = None

#     class Settings:
#         collection = "users"

class UserModel(BaseModel):
    cnic: int
    forename: str
    surname: str
    address: str
    email: str
    password: Optional[str]