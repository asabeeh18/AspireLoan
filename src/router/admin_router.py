from db_layer import admin_actions
from fastapi import APIRouter, HTTPException
from model.db_model import State
from model.request_model import LoanList, ResponseLoanModel
from starlette import status

router = APIRouter()


@router.get("/pending_loans/", response_model=LoanList)
async def get_pending_loans():
    return admin_actions.get_pending_loans()


@router.post("/action_pending/", response_model=ResponseLoanModel)
async def action_pending(loan_id: int, action: State):
    if action is not State.REJECTED and action is not State.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid action chosen: {action} ",
        )
    x = admin_actions.action_pending_loan(loan_id, action)
    return ResponseLoanModel.model_validate(x)
