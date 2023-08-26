from datetime import timedelta

from playhouse.shortcuts import model_to_dict

from src.model.db_model import User, Loan, State, db, Repayment
from src.model.request_model import UserModel, UserResponse, LoanModel, RepayResponse, RepayList


def new_user(user: UserModel):
    u = User(name=user.name, email=user.email, password=user.password)
    u.save()
    return u


def get_user(id: int):
    users = User.select().where(User.user_id == id).get()
    # posts = Post.select() \
    #     .join(User) \
    #     .switch(Post) \
    #     .join(PostTag) \
    #     .join(Tag) \
    #     .paginate(10, 1)
    # for post in posts:
    #     print(PostModel.from_orm(post))
    #     tags = [TagModel.from_orm(tag) for tag in post.tags]
    #     print("Tags: " + ", ".join([tag.name for tag in tags]))

    return users


def create_loan(loan: LoanModel):
    l = Loan(**loan.model_dump())
    loan_user = User.select().where(loan.user_id == User.user_id).get()
    l.user_id = loan_user
    l.state = State.PENDING.value
    repay = loan.amount / loan.term
    repay_sched = []
    with db.atomic():
        l.save()
        for i in range(loan.term):
            Repayment.create(
                date=loan.start_date + timedelta(days=(i + 1) * 7),
                payment=repay,
                state=State.PENDING.value,
                loan=l)

    ###

    l = model_to_dict(l)
    l['user_id'] = l['user_id']['user_id']
    return l

def repay_scedule(loan_id):
    loan=Loan.select().where(Loan.loan_id==loan_id).get()
    if loan:
        repay=Repayment.select().where(Repayment.loan==loan)
        l=[]
        for r in repay:
            l.append(RepayResponse.model_validate(r))
        return RepayList(schedule=l)