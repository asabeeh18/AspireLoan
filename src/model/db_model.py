from enum import Enum

from peewee import *

db = SqliteDatabase("AspireLoan.db")


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()


class Admin(Person, BaseModel):
    pass


class User(Person):
    user_id = AutoField()


class State(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    PAID = "PAID"
    REJECTED = "REJECTED"


class Loan(BaseModel):
    loan_id = AutoField()
    amount = FloatField()
    term = IntegerField()
    start_date = DateField()
    state = CharField()
    user = ForeignKeyField(User, backref="Loan")


class Repayment(BaseModel):
    date = DateField()
    payment = FloatField()
    state = CharField()
    loan = ForeignKeyField(Loan, backref="Repayment")


def initialize_db():
    db.connect()
    db.create_tables([User, Loan, Repayment], safe=True)
    db.close()
