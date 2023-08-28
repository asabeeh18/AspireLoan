from fastapi import HTTPException
from starlette import status

from model.db_model import Loan, State, Repayment


def get_pending_with_id(loan_id):
    loan = Loan.select().where(Loan.loan_id == loan_id, Loan.state == State.PENDING)
    if not loan:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"No loan found with id: {loan_id} or loan not in pending state", )
    return loan.get()


def get_loan_and_repay(loan_id: int):
    """
    Returns the loan object and all repayment currently due, raises exception otherwise
    :param loan_id: Unique identifier of the loan
    :return:
    """

    loan = get_loan(loan_id)
    # Need to make sure loan is approved to accept payment
    if loan.state != State.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Loan id {loan_id} with state {loan.state} is not allowed for repayment",
        )

    # Select all the pending payments for this loan id
    # Use .for_update() after select if supported by DB to lock rows
    repay = Repayment.select().where(
        Repayment.loan == loan_id, Repayment.state == State.PENDING
    )

    if not repay:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"No repayment found for Loan id {loan_id}",
        )
    return loan, repay


def get_loan(loan_id):
    loan = Loan.select().where(Loan.loan_id == loan_id)  # .for_update()
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Loan with id {loan_id} not found",
        )
    return loan.get()
