from django.contrib import admin
from .models import Transaction
# Register your models here.


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', '_id', 'order_id', 'order_type', 'amount', 'status','paid' ,'date')
    list_display_links = ('id',)
    list_filter = ('status', 'paid')
    search_fields = ['order_id', 'status','order_type','id','_id']

admin.site.register(Transaction,TransactionAdmin)