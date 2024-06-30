from typing import Optional
from beanie import Document
from pydantic import BaseModel, Field


class User(Document):
    cnic: int = Field(..., example=3310487812709)
    forename: str = Field(..., example="Saad")
    surname: str = Field(..., example="Abdur Razzaq")
    address: str = Field(..., example="Paradise Valley Phase 1, Faisalabad")
    email: str = Field(..., example="saad@cyberevangelists.com")
    password: str = Field(..., example="saad@1234")

    class Settings:
        collection = "User"


class UserModel(BaseModel):
    cnic: int = Field(..., example=3310407495057)
    forename: str = Field(..., example="Taha")
    surname: str = Field(..., example="Abdur Razzaq")
    address: str = Field(..., example="Paradise Valley Phase 1, Faisalabad")
    email: str = Field(..., example="taha@bitsgenesis.com")
    password: str = Field(..., example="taha@1234")


class UserUpdateModel(BaseModel):
    forename: Optional[str] = Field(None, example="Wasif")
    surname: Optional[str] = Field(None, example="Muhammad")
    address: Optional[str] = Field(None, example="Doha, Qatar")
    email: Optional[str] = Field(None, example="wasif@webaurai.com")
    password: Optional[str] = Field(None, example="wasif@1234")
