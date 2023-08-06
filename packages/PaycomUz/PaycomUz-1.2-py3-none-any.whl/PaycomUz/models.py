from django.db import models


class Transaction(models.Model):
    choice_status = (('processing','processing'),('success','success'),('failed','failed'))
    _id = models.CharField(max_length=255)
    request_id = models.CharField(max_length=255)
    order_id = models.IntegerField()
    order_type = models.CharField(max_length=255,blank=True,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.IntegerField(blank=True,null=True)
    status = models.CharField(choices=choice_status,default='processing',max_length=255)
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    error = models.TextField(default='None',max_length=255,blank=True,null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None,*args,**kwargs):
        if self._id == 'error_response':
            last = Transaction.objects.filter(_id__startswith='error_response').last()
            if not last:
                self._id = 'error_response1'
                super(Transaction,self).save(*args,**kwargs)
            else:
                text = last._id.split('error_response')
                number = int(text[1]) + 1
                generate_code = 'error_response' + str(number)
                self._id = generate_code
                super(Transaction, self).save(*args, **kwargs)
        else:
            super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)