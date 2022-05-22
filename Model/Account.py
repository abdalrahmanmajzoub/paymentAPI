import datetime as dt
from marshmallow import Schema, fields,validate

from Model.AccountType import accountType
from Model.CurrencyCode import currencyCode

class Account:
    balance = 0.00
    def __init__(self,accountNumber,currencyCode,ownerName, type ):
        self.accountNumber=accountNumber
        self.currencyCode=currencyCode
        self.ownerName=ownerName
        self.type=type

    def __repr__(self):
        return "<Account(ownerName={self.ownerName!r})>".format(self=self)

class AccountSchema(Schema):
    accountNumber = fields.Int()
    accountType = fields.Str(validate=validate.OneOf([accountType.individual.value,accountType.corporate.value]))
    currencyCode = fields.Str(validate=validate.OneOf([currencyCode.TRY.value,currencyCode.USD.value,currencyCode.EUR.value]))
    ownerName = fields.Str()
    balance = fields.Decimal(2,as_string=True)
    type = fields.Str()

def make_user(self, data, **kwargs):
        return Account(**data)

