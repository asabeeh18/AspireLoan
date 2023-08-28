from fastapi import HTTPException
from playhouse.shortcuts import model_to_dict
from starlette import status

from model.db_model import Loan, State
from model.request_model import ResponseLoanModel, LoanList


def get_pending_with_id(loan_id):
    loan = Loan.select().where(Loan.loan_id == loan_id, Loan.state == State.PENDING)
    if not loan:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"No loan found with id: {loan_id} or loan not in pending state", )
    return loan.get()


def get_pending_loans() -> LoanList:
    """
    Returns all the laons in pending state
    :return: LoanList object which contains all Loans currently pending
    """
    loans = Loan.select().where(Loan.state == State.PENDING.value).dicts()
    res = []
    for l in loans:
        res.append(ResponseLoanModel.model_validate(l))

    return LoanList(loans=res)


def action_pending_loan(loan_id: int, action: State):
    """
    Updates the state of loan with the action
    :param loan_id: Unique id of the loan
    :param action: Only allowed APPROVED or REJECTED
    :return:
    """
    loan = get_pending_with_id(loan_id)

    loan = loan.get()
    loan.state = action
    loan.save()

    loan = model_to_dict(loan)
    loan["user_id"] = loan["user"]["user_id"]
    del loan["user"]
    return loan
