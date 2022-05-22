from marshmallow import Schema, fields,validate


class Withdraw():
    def __init__(self,accountNumber,amount):
        self.accountNumber = accountNumber
        self.amount = amount

def __repr__(self):
        return "<Payment(accountNumber={self.accountNumber!r})>".format(self=self)
        

class WithdrawShcema(Schema):
    accountNumber = fields.Int(Required=True)
    amount = fields.Decimal(2,as_string=True,validate=validate.Range(min=0.01))


def make_Withdraw(self, data, **kwargs):
    return Withdraw(**data)