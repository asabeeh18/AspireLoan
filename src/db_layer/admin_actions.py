from fastapi import HTTPException
from playhouse.shortcuts import model_to_dict
from starlette import status

from src.model.db_model import Loan, State
from src.model.request_model import LoanResponse, LoanList


def get_pending_loans():
    loans = Loan.select().where(Loan.state == State.PENDING.value).dicts()
    # l = LoanList(loans=
    # [
    #     LoanResponse.model_validate(loan) for loan in loans
    # ]
    # )
    res = []
    for l in loans:
        res.append(LoanResponse.model_validate(l))

    return LoanList(loans=res)


def action_pending_loan(loan_id: int, action: State):
    loan = Loan.select().where(Loan.loan_id == loan_id)
    if loan:
        loan=loan.get()
        if loan.state == State.PENDING.value:
            loan.state = action
            loan.save()
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f'Loan is in state {State(loan.state)} and cannot be moved')
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'No loan found with id: {loan_id}')
    loan = model_to_dict(loan)
    loan['user_id'] = loan['user_id']['user_id']
    return loan
