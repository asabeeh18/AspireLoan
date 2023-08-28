from datetime import date
from typing import List

from pydantic import SecretStr, Field, BaseModel, EmailStr

from src.model.db_model import State


class UserModel(BaseModel):
    class Config:
        from_attributes = True

    name: str
    email: EmailStr
    password: str


class UserResponse(UserModel):
    password: SecretStr = Field(..., exclude=True)


class Loan():
    amount: float
    term: int
    start_date: date


class RequestLoanModel(BaseModel, Loan):
    user_token: str

    class Config:
        from_attributes = True


class ResponseLoanModel(BaseModel, Loan):
    loan_id: int

    class Config:
        from_attributes = True

class LoanList(BaseModel):
    class Config:
        from_attributes = True

    loans: List[ResponseLoanModel]


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
