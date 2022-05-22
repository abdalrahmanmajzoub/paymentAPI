from flask import Flask,jsonify, request
from marshmallow import  ValidationError

from Model.Account import Account,AccountSchema
from Model.AccountType import accountType
from Model.CurrencyCode import currencyCode
from Model.Payment import PaymentShcema
from Model.Transaction import Transaction,TransactionShcema
from Model.Deposit import Deposit,DepositShcema
from Model.Withdraw import Withdraw,WithdrawShcema

app = Flask(__name__)
Ac1 = Account(6200,currencyCode.EUR.value,'safouh',accountType.individual.value)
Ac1.balance = 600.00

Ac2 = Account(6201,currencyCode.TRY.value,'abd',accountType.corporate.value)
Ac3 = Account(6202,currencyCode.USD.value,'hadi',accountType.individual.value)
Ac4 = Account(6203,currencyCode.EUR.value,'marwan',accountType.corporate.value)
accountsList= [Ac1,Ac2,Ac3,Ac4]
transactionList =[]





err_record_not_found = {'Messege':'Account with the same accountNumber not exists'}
err_account_exist = {'Messege':"Account with the same accountNumber already exists"}
err_senderAccount_not_found = {'Messege':'Sender account not exists'}
err_receiverAccount_not_found = {'Messege':'Reciver account not exists'}
err_senderAccount_is_not_ind = {'Messege':'Sender account is not individual'}
err_receiverAccount_is_not_corp = {'Messege':'Reciver account is not corporate'}
err_no_enough_balance = {'Messege':'account has no enough balance'}
err_nonIndv_acc ={'Messege':'can not perform this kind of transaction with this account'}
success_add = {'Messege':'Account Succesfully Created'}
success_op = {'Messege':'Success'}


def account_exist(accountNumber: int):
    for account in accountsList:
        if account.accountNumber == accountNumber:
            return True
        else:
            continue
            return False

def find_account_byID(accountNumber: int):
    for account in accountsList:
        if account.accountNumber == int(accountNumber):
            return account
        else:
            continue

def sender_is_indv(senderAccount:int):
    for account in accountsList:
        if account.accountNumber == int(senderAccount) and account.type == accountType.individual.value:
            return account
        else:
            continue

def reciver_is_corp(receiverAccount:int):
    for account in accountsList:
        if account.accountNumber == int(receiverAccount) and account.type == accountType.corporate.value:
            return account
        else:
            continue
      


@app.route("/")
def hello_world():
  return "Hello, World!"



@app.route('/account/<int:accountNumber>', methods=['GET'])
def get_account(accountNumber):
    res =[]
    schema = AccountSchema()
    acc =find_account_byID(accountNumber)
    
    if acc is not None:
        res.append(schema.dump(acc))
        return jsonify(res),200
    else:
        return jsonify(err_record_not_found),400


@app.route('/account', methods=['POST'])
def add_account():
    data = request.get_json()
    try:
        account = AccountSchema().load(data)
    except ValidationError as err:
            return jsonify(err.messages),400
        
        
    if account_exist(int(account['accountNumber'])):
        return jsonify(err_account_exist),400
    else:
        accountsList.append(Account(account['accountNumber'],account['currencyCode'],account['ownerName'],account['accountType']))
        return jsonify(success_add),200


@app.route('/payment',methods=['POST'])
def add_payment():

    data = request.get_json()
    try:
        payment = PaymentShcema().load(data)
    except ValidationError as err:
        return jsonify(err.messages),400
    senderData = find_account_byID(int(payment['senderAccount']))
    reciverData = find_account_byID(int(payment['reciverAccount']))



    if (senderData is None):
        return jsonify(err_senderAccount_not_found),400
    elif(reciverData is None):
        return jsonify(err_receiverAccount_not_found),400
    elif(accountsList[accountsList.index(senderData)].type != accountType.individual.value):
        return jsonify(err_senderAccount_is_not_ind)
    elif(accountsList[accountsList.index(reciverData)].type != accountType.corporate.value):
        return jsonify(err_receiverAccount_is_not_corp),400
    elif(senderData.balance < payment['amount']):
        return jsonify(err_no_enough_balance),400
    else:
        accountsList[accountsList.index(senderData)].balance =accountsList[accountsList.index(senderData)].balance - float(payment['amount'])
        accountsList[accountsList.index(reciverData)].balance = accountsList[accountsList.index(reciverData)].balance + float(payment['amount'])
        transactionList.append(Transaction(payment['senderAccount'],payment['amount'],'payment'))
        transactionList.append(Transaction(payment['reciverAccount'],payment['amount'],'payment'))
        return jsonify(success_op),200



@app.route('/deposit',methods=['POST'])
def add_deposit():
####try 
    try:
        deposit = DepositShcema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages),400
    accountData = find_account_byID(int(deposit['accountNumber']))

    if (accountData is None):
        return jsonify(err_record_not_found),400
    elif(accountsList[accountsList.index(accountData)].type != accountType.individual.value):
        return jsonify(err_nonIndv_acc),400
    else:
        accountsList[accountsList.index(accountData)].balance = accountsList[accountsList.index(accountData)].balance + float(deposit['amount'])
        transactionList.append(Transaction(deposit['accountNumber'],deposit['amount'],'deposit'))
        return jsonify(success_op),200



@app.route('/withdraw',methods=['POST'])
def add_withdraw():
    try:
        withdraw = WithdrawShcema().load(request.get_json())
    except ValidationError as err:
        return(jsonify(err.messages)),400
    accountData = find_account_byID(int(withdraw['accountNumber']))

    if (accountData is None):
        return jsonify(err_record_not_found),400
    elif(accountsList[accountsList.index(accountData)].type != accountType.individual.value):
        return jsonify(err_nonIndv_acc),400
    elif(accountsList[accountsList.index(accountData)].balance < withdraw['amount']):
        return jsonify(err_no_enough_balance),400
    else:
        accountsList[accountsList.index(accountData)].balance = accountsList[accountsList.index(accountData)].balance - float(withdraw['amount'])
        transactionList.append(Transaction(withdraw['accountNumber'],withdraw['amount'],'withdraw'))
        return jsonify(success_op),200




@app.route('/accounting/<int:accountNumber>',methods=['GET'])
def accounting(accountNumber):
    res =[]
    schema = TransactionShcema(many=True)
    accountData = find_account_byID(int(accountNumber))
    if accountData is None:
        return jsonify(err_record_not_found),400
    else:
        transactions = schema.dump(filter(lambda t: t.accountNumber == accountNumber, transactionList))
        return jsonify(transactions),200



if __name__ == "__main__":  
  app.run(host='127.0.0.1', port=5050)