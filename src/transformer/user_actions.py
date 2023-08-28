from datetime import timedelta

from fastapi import HTTPException
from starlette import status

from libs.login_manager import register_user_session, get_user_id_from_token
from model.db_model import User, Loan, State, db, Repayment
from model.request_model import (
    UserModel,
    RequestLoanModel,
    RepayResponse,
    RepayList,
)
from transformer.db_accessor import get_loan_and_repay, get_loan


def new_user(user: UserModel):
    """
    Function to create a new user and save it in db
    :param user: User model object which contains basic user details
    :return: User object with user_id
    """
    u = User(name=user.name, email=user.email, password=user.password)
    u.save()
    return u


def get_user_with_id(user_id):
    user = User.select().where(User.user_id == user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"No user found with id: {user_id}",
        )
    return user.get()


def get_user(user_id: int) -> User:
    """
    Retrieve user object from db
    :param user_id: user_id
    :return:
    """
    return get_user_with_id(user_id)


def create_loan(loan: RequestLoanModel):
    """

    :param loan: Loan model which has the loan details from the user
    :return:
    """
    user_id = get_user_id_from_token(loan.user_token)
    loan_db = Loan(**loan.model_dump())

    # Get the user object for new loan
    loan_user = (
        User.select()
            .where(get_user_id_from_token(loan.user_token) == User.user_id)
            .get()
    )

    loan_db.user = loan_user
    loan_db.state = State.PENDING.value

    # Create repayment objects for this loan
    repay = loan.amount / loan.term
    with db.atomic():
        loan_db.save()
        for i in range(loan.term):
            Repayment.create(
                date=loan.start_date + timedelta(days=(i + 1) * 7),
                payment=repay,
                state=State.PENDING.value,
                loan=loan_db,
            )
    return loan_db


def repay_schedule(loan_id, user_token):
    loan = get_loan(loan_id)
    if loan.user.user_id != get_user_id_from_token(user_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with token {user_token} is forbidden to access loan with id {loan_id}",
        )

    repay = Repayment.select().where(Repayment.loan == loan)
    l = []
    for r in repay:
        l.append(RepayResponse.model_validate(r))
    return RepayList(schedule=l)


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


def login(email: str, password: str):
    """
    Log ins the user and stores the session key wit user id
    :param email:
    :param password:
    :return: token string which identifies user for some APIs
    """
    user = User.select(User.user_id).where(
        User.email == email, User.password == password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User {email} does not exist or incorrect password",
        )
    user_id = user.scalar()
    token = register_user_session(user_id)
    return token
