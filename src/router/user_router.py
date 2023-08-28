from fastapi import APIRouter

from model.request_model import (
    UserModel,
    UserResponse,
    RequestLoanModel,
    ResponseLoanModel,
    RepayList,
    RepayResponse,
)
from transformer import user_actions

router = APIRouter()


@router.post("/create/", response_model=UserResponse)
async def create_user(user: UserModel):
    return user_actions.new_user(user)


@router.get("/get/", response_model=UserResponse)
async def get_user(id: int):
    user = user_actions.get_user(id)
    return UserResponse.model_validate(user)


@router.post("/new_loan", response_model=ResponseLoanModel)
async def new_loan(loan: RequestLoanModel):
    l = user_actions.create_loan(loan)
    return ResponseLoanModel.model_validate(l)


@router.get("/repay_scehdule/", response_model=RepayList)
async def get_repayment_schedule(loan_id: int, user_token: str):
    return user_actions.repay_schedule(loan_id, user_token)


@router.get("/repay_loan/", tags=["users"], response_model=RepayResponse)
async def repay_loan(loan_id: int):
    repay_status = user_actions.repay_loan(loan_id)
    return RepayResponse.model_validate(repay_status)


@router.get("/login/", tags=["users"])
async def login(email: str, password: str):
    return user_actions.login(email, password)
