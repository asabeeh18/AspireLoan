from datetime import date
from enum import Enum
from typing import Optional, List

import pydantic
from pydantic import SecretStr, Field, BaseModel, EmailStr

from src.model import db_model
from src.model.db_model import User, State


class UserModel(BaseModel):
    class Config:
        from_attributes = True

    name: str
    email: EmailStr
    password: str


class UserResponse(UserModel):
    password: SecretStr = Field(..., exclude=True)


class LoanModel(BaseModel):
    amount: float
    term: int
    start_date: date
    user_token: str

    class Config:
        from_attributes = True


class LoanResponse(LoanModel):
    loan_id: int


class LoanList(BaseModel):
    class Config:
        from_attributes = True

    loans: List[LoanResponse]


class RepayResponse(BaseModel):
    class Config:
        from_attributes = True

    date: date
    payment: float
    state: State
    loan_id: int


class RepayList(BaseModel):
    class Config:
        from_attributes = True

    schedule: List[RepayResponse]
