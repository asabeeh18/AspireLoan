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
    user_id: int


class Loan(BaseModel):
    amount: float
    term: int
    start_date: date

    class Config:
        from_attributes = True


class RequestLoanModel(Loan):
    user_token: str


class ResponseLoanModel(Loan):
    loan_id: int


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
