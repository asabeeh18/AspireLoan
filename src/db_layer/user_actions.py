from datetime import timedelta

from fastapi import HTTPException
from playhouse.shortcuts import model_to_dict
from starlette import status

from src.model.db_model import User, Loan, State, db, Repayment
from src.model.request_model import (
    UserModel,
    RequestLoanModel,
    RepayResponse,
    RepayList,
)


def new_user(user: UserModel):
    u = User(name=user.name, email=user.email, password=user.password)
    u.save()
    return u


def get_user(id: int):
    users = User.select().where(User.user_id == id).get()
    return users


def create_loan(loan: RequestLoanModel):
    if loan.user_token not in user_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User is not logged in or incorrect token",
        )
    l = Loan(**loan.model_dump())
    loan_user = User.select().where(user_session[loan.user_token] == User.user_id).get()

    l.user = loan_user
    l.state = State.PENDING.value
    repay = loan.amount / loan.term
    with db.atomic():
        l.save()
        for i in range(loan.term):
            Repayment.create(
                date=loan.start_date + timedelta(days=(i + 1) * 7),
                payment=repay,
                state=State.PENDING.value,
                loan=l,
            )
    return l


def loan_to_loan_model(l):
    l = model_to_dict(l)
    l["user_id"] = l["user_id"]["user_id"]
    return l


def get_loan(loan_id):
    loan = Loan.select().where(Loan.loan_id == loan_id)  # .for_update()
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Loan with id {loan_id} not found",
        )
    return loan.get()


def repay_scedule(loan_id, user_token):
    loan = get_loan(loan_id)
    if loan.user.user_id != user_session[user_token]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with token {user_token} is forbidden to access loan with id {loan_id}",
        )

    repay = Repayment.select().where(Repayment.loan == loan)
    l = []
    for r in repay:
        l.append(RepayResponse.model_validate(r))
    return RepayList(schedule=l)


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

    # Use .for_update() after select if supported by DB to lock rows
    repay = Repayment.select().where(
        Repayment.loan == loan_id and Repayment.state == State.PENDING
    )

    if not repay:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"No repayment found for Loan id {loan_id}",
        )
    return loan, repay


def repay_loan(loan_id: int) -> Repayment:
    """
    Returns the repayment object of the loan id for which loan was paid

    :param loan_id: Unique identifier of the loan
    :return: Repayment object reflecting if the loan was paid
    """
    loan, repay = get_loan_and_repay(loan_id)
    x = repay.select().order_by(Repayment.date.asc()).get()
    x.state = State.PAID
    x.save()

    # Update loan status to paid if all repayments are complete
    if all(i.state == State.PAID for i in repay):
        loan.state = State.PAID
        loan.save()

    return x


user_session = {}


def login(email: str, password: str):
    user = User.select(User.user_id).where(
        User.email == email, User.password == password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User {email} does not exist or incorrect password",
        )
    user_id = user.scalar()
    token = str(hash(str(user_id)))
    user_session[token] = user_id
    return token
