#from typing_extensions import Required
from marshmallow import Schema, fields,validate


class Payment():
    def __init__(self,senderAccount,reciverAccount,amount):
        self.senderAccount = senderAccount
        self.reciverAccount = reciverAccount
        self.amount = amount

def __repr__(self):
        return "<Payment(accountNumber={self.accountNumber!r})>".format(self=self)
        

class PaymentShcema(Schema):
    senderAccount = fields.Int(Required=True)
    reciverAccount = fields.Int(Required=True)
    amount = fields.Decimal(2,as_string=True,validate=validate.Range(min=0.01))


def make_Payment(self, data, **kwargs):
    return Payment(**data)