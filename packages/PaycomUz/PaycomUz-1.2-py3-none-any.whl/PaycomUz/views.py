from rest_framework.views import APIView
from importlib import import_module
from rest_framework.response import Response
from .models import Transaction
from django.conf import settings
import time
from .status import *
from .permissions import Paycom_Permissions
accounts_key = settings.PAYCOM_SETTINGS['ACCOUNTS']
import_class = import_module(settings.PAYCOM_SETTINGS['PATH_CLASS'])
from rest_framework.decorators import permission_classes, authentication_classes

@authentication_classes([])
@permission_classes([Paycom_Permissions])
class MerchantAPIView(APIView):

    def __init__(self):
        self.function = import_class
        self.amount = None
        self.order_id = None
        self.order_type = None
        self._id = None
        self.time = None
        self.request_id = None
        self.transaction_id = None
        self.error_code = None
        self.message = None
        self.data = None
        self.reply = None
        super().__init__()

    def post(self,request):
        self.data = request.data
        self.check_method()
        return Response(self.reply)

    def check_perform_transaction(self): #1
        answer = self.function.Paycom(order_id=self.order_id,
                             order_type=self.order_type,
                             amount=self.amount).check_order()
        if answer == ORDER_FOUND:
            self.reply = ORDER_FOUND_MESSAGE
        elif answer == ORDER_NOT_FOND:
            self.error_code = ORDER_NOT_FOND
            self.message = ORDER_NOT_FOND_MESSAGE
            self.error_response()
        elif answer == INVALID_AMOUNT:
            self.error_code = INVALID_AMOUNT
            self.message = INVALID_AMOUNT_MESSAGE
            self.error_response()
        else:
            self.error_code = ORDER_NOT_FOND
            self.message = ORDER_NOT_FOND_MESSAGE
            self.error_response()

    def check_method(self):
        if self.data['method'] == 'CheckPerformTransaction':
            self.check_perform_transaction_parser()
            self.check_perform_transaction()
        elif self.data['method'] == 'CreateTransaction':
            self.create_transaction_parser()
            self.search_transaction()
        elif self.data['method'] == 'PerformTransaction':
            self.perform_transaction_parser()
            self.search_perform()


    def transaction_create(self):
        create = Transaction.objects.create(
            _id=self._id,
            order_id=self.order_id,
            order_type=self.order_type,
            amount=self.amount/100,
            state=1,
            request_id=self.request_id
        )
        self.transaction_id = create.pk

    def search_transaction(self):
        try:
            get = Transaction.objects.get(_id=self._id)
            if get.state == 1:
                self.transaction_id = get.id
                self.success_create_transaction()
            else:
                self.error_code = UNABLE_TO_PERFORM_OPERATION
                self.message = UNABLE_TO_PERFORM_OPERATION_MESSAGE
                self.error_response()
        except:
            self.transaction_create()
            self.success_create_transaction()

    def search_perform(self):
        try:
            get = Transaction.objects.get(_id=self._id)
            self.transaction_id = get.id
            if get.state == 1:
                self.update_transaction()
                self.success_perform()

            elif get.state == 2:
                self.success_perform()
            else:
                self.error_code = UNABLE_TO_PERFORM_OPERATION
                self.message = UNABLE_TO_PERFORM_OPERATION_MESSAGE
                self.error_response()
        except:
            self.error_code = TRANSACTION_NOT_FOND
            self.message = TRANSACTION_NOT_FOND_MESSAGE
            self.error_response()

    def update_transaction(self):
        get = Transaction.objects.get(pk=self.transaction_id)
        get.paid = True
        get.status = 'success'
        get.state = 2
        get.save()

    def check_perform_transaction_parser(self):
        if accounts_key['KEY2'] == None:
            self.amount = self.data['params']['amount']
            self.order_id = self.data['params']['account'][accounts_key['KEY1']]
            self.request_id = self.data['id']
        else:
            self.amount = self.data['params']['amount']
            self.order_id = self.data['params']['account'][accounts_key['KEY1']]
            self.order_type = self.data['params']['account'][accounts_key['KEY2']]
            self.request_id = self.data['id']

    def create_transaction_parser(self):
        if accounts_key['KEY2'] == None:
            self.order_id = self.data['params']['account'][accounts_key['KEY1']]
            self.amount = self.data['params']['amount']
            self._id = self.data['params']['id']
            self.request_id = self.data['id']
        else:
            self.order_id = self.data['params']['account'][accounts_key['KEY1']]
            self.order_type = self.data['params']['account'][accounts_key['KEY2']]
            self.amount = self.data['params']['amount']
            self._id = self.data['params']['id']
            self.request_id = self.data['id']

    def perform_transaction_parser(self):
        self.request_id = self.data['id']
        self._id = self.data['params']['id']

    def success_create_transaction(self):
        date_time = lambda: int(round(time.time() * 1000))
        self.reply = {
            "result" : {
                "create_time" :date_time(),
                "transaction" : str(self.transaction_id),
                "state" : 1
            }
        }

    def success_perform(self):
        date_time = lambda: int(round(time.time() * 1000))
        self.reply = {
            "result":{
                "transaction":str(self.transaction_id),
                "perform_time":date_time(),
                "state":2
            }
        }

    def error_response(self):
        self.reply = {
            "error":{
                "code":self.error_code,
                "id":self.request_id,
                "message":self.message
            }
        }
