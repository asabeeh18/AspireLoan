from fastapi import APIRouter

from src.db_layer import user_actions
from src.model.db_model import User
from src.model.request_model import UserModel, UserResponse, LoanModel, LoanResponse, RepayList

router = APIRouter()


@router.post("/create/", response_model=UserResponse)
async def create_user(user: UserModel):
    return user_actions.new_user(user)


@router.get("/get/", response_model=UserResponse)
async def get_user(id: int):
    user = user_actions.get_user(id)
    return UserResponse.model_validate(user)


@router.post("/new_loan", response_model=LoanResponse)
async def new_loan(loan: LoanModel):
    l= user_actions.create_loan(loan)
    return LoanResponse.model_validate(l)



@router.get("/repay_scehdule/", response_model=RepayList)
async def get_repayment_schedule(loan_id: int):
    return user_actions.repay_scedule(loan_id)



@router.get("/repay_loan/", tags=["users"])
async def repay_loan(loan_id: int):
    return user_actions.repay_loan(loan_id)

