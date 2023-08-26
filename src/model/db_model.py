from enum import Enum

from peewee import *

db = SqliteDatabase('AspireLoan.db')


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    name = CharField()
    email = CharField()
    password = CharField()
    """
    'full_name',
        'email',
        'password',
        'signup_role',
        'signup_looking_for',
        'heard_through',
        'email_verified_at',
        """


class Admin(Person, BaseModel):
    pass


class User(Person):
    user_id = AutoField()
    pass
    # name = CharField()
    # email = CharField()
    # password = CharField()
    #
    # class Meta:
    #     database = db  # This model uses the "people.db" database.


class State(str, Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    PAID = 'PAID'
    REJECTED = 'REJECTED'


class Loan(BaseModel):
    loan_id = AutoField()
    amount = FloatField()
    term = IntegerField()
    start_date = DateField()
    #due_date = DateField()

    state = CharField()  # ForeignKeyField(State, backref='Loan')
    user_id = ForeignKeyField(User, backref='Loan')
    #
class Repayment(BaseModel):
    date = DateField()
    payment = FloatField()
    state = CharField()
    loan = ForeignKeyField(Loan, backref='Repayment')


def initialize_db():
    db.connect()
    db.create_tables([User, Loan, Repayment], safe=True)
    db.close()
