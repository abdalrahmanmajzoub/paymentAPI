import datetime as dt
#from typing_extensions import Required
from marshmallow import Schema, fields,validate
from Model.TransactionType import transactionType

class Transaction():
  def __init__(self,accountNumber, amount, transactionType):
    self.accountNumber = accountNumber
    self.amount = amount
    self.transactionType  = transactionType
    self.createdAt = dt.datetime.now()

def __repr__(self):
        return "<Transaction(accountNumber={self.accountNumber!r})>".format(self=self)

class TransactionShcema(Schema):
    accountNumber = fields.Int(Required=True)
    amount = fields.Decimal(2,as_string=True)
    transactionType = fields.Str(validate=validate.OneOf([transactionType.payment.value,transactionType.deposit.value,transactionType.withdraw.value]))
    createdAt = fields.DateTime(Required=True)

def make_transaction(self, data, **kwargs):
    return Transaction(**data)