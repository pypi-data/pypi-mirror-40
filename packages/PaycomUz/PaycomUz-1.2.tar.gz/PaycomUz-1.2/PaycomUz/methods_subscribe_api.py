import requests
import json
from django.conf import settings
from .models import Transaction
from importlib import import_module
#-------------------------------------------------------------#
HOST = settings.PAYCOM_SETTINGS['HOST']  #URL PAYME
AUTHORIZATION = settings.PAYCOM_SETTINGS['ID']  #TOKEN
HEADERS = {'Content-type': 'application/json' , 'X-Auth':AUTHORIZATION} #HEADERS
accounts_key = settings.PAYCOM_SETTINGS['ACCOUNTS']
import_class = import_module(settings.PAYCOM_SETTINGS['PATH_CLASS'])
#---------------------------------------------------------------#


class Subcribe:
    def __init__(self,order_id=None,amount=None,token=None,order_type=None):
        self.order_id = order_id
        self.amount = amount
        self.token = token
        self.order_type = order_type
        self._id = None
        self.transaction_id = None
        self.response = None
        self.function = import_class

    def receipts_create(self):
        response = {
            "id":123,
            "method": "receipts.create",
            "params": {
                "amount": self.amount * 100,
                "account": {
                    accounts_key['KEY1']:self.order_id,
                    accounts_key['KEY2']:self.order_type
                }
            }
        }
        try:
            r = requests.post(url=HOST,data=json.dumps(response),headers=HEADERS)
            self.checK_request_receipts_create(json.loads(r.text))
        except:
            self.internet_error()
        return self.response

    def receipts_pay(self):
        response = {
            "id": 123,
            "method": "receipts.pay",
            "params": {
                "id": self._id,
                "token": self.token
            }
        }
        try:
            r = requests.post(url=HOST,data=json.dumps(response),headers=HEADERS)
            self.check_request_receipts_pay(data=json.loads(r.text))
        except:
            self.internet_error()

    def checK_request_receipts_create(self,data=None):
        if 'error' in data:
            self.error_transaction_response(data)
        else:
            self._id = data['result']['receipt']['_id']
            self.receipts_pay()

    def check_request_receipts_pay(self,data=None):
        if 'error' in data:
            self.error_transaction_response(data)
        else:
            self.response = {
                "_id":data['result']['receipt']['_id'],
                "paid":True,
                "status":"success",
                "error":None
            }

    def error_transaction_response(self,data=None):
        error_transaction = Transaction.objects.create(
            _id="error_response",
            order_id=self.order_id,
            order_type=self.order_type,
            amount=self.amount,
            state=0,
            status="failed",
            error=data['error'],
            request_id="0000000000000000000000"
        )
        self.response = {
            "_id": error_transaction._id,
            "paid": False,
            "status": "failed",
            "error": data
        }

    def internet_error(self):
        self.response = {
            "_id": None,
            "paid": False,
            "status":"failed",
            "error": "your internet isn't working",
        }