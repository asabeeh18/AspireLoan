from fastapi import APIRouter, HTTPException
from starlette import status

from src.db_layer import admin_actions
from src.model.db_model import State
from src.model.request_model import LoanList, LoanResponse

router = APIRouter()


@router.get("/pending_loans/", response_model=LoanList)
async def get_pending_loans():
    return admin_actions.get_pending_loans()


@router.post("/action_pending/", response_model=LoanResponse)
async def action_pending(loan_id: int, action: State):
    if action is not State.REJECTED and action is not State.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid action chosen: {action} ",
        )
    x = admin_actions.action_pending_loan(loan_id, action)
    return LoanResponse.model_validate(x)
