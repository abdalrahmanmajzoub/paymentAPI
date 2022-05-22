#from typing_extensions import Required
from marshmallow import Schema, fields,validate


class Deposit():
    def __init__(self,accountNumber,amount):
        self.accountNumber = accountNumber
        self.amount = amount

def __repr__(self):
        return "<Payment(accountNumber={self.accountNumber!r})>".format(self=self)
        

class DepositShcema(Schema):
    accountNumber = fields.Int(Required=True)
    amount = fields.Decimal(2,as_string=True,validate=validate.Range(min=0.01))


def make_Payment(self, data, **kwargs):
    return Deposit(**data)