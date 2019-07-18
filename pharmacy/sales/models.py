from django.db import models
from items.models import Item
# Create your models here.
class Invoice(models.Model):
    c_name= models.CharField(max_length=60,null=True)
    c_phone=models.CharField(max_length=10,null=True)
    date=models.DateField()
    gtotal=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
    def __str__(self):
        return str(self.id)

class Invoice_items(models.Model):
    invoice_id=models.ForeignKey(Invoice,on_delete=models.CASCADE,null=True)
    item_id=models.ForeignKey(Item,on_delete=models.SET_NULL,null=True)
    no_of_units=models.IntegerField()
    loose_qty=models.DecimalField(max_digits=10,decimal_places=2)
    mrp=models.DecimalField(max_digits=10,decimal_places=2)
    batchno=models.CharField(max_length=10,null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    exp_date=models.DateField(null=True)
    def __str__(self):
        return str(self.id)