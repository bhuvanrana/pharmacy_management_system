from django.db import models
from django.utils import timezone
# Create your models here.
from accounts.models import Supplier
from items.models import Item

class Supply_product(models.Model):
    supplier_id=models.ForeignKey(Supplier,on_delete=models.CASCADE)
    item_id=models.ForeignKey(Item,on_delete=models.CASCADE)
    purchase_price=models.DecimalField(max_digits=10,decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2,default=0)
    def __str__(self):
        return str(self.id)

class Order(models.Model):
    supplier_id = models.ForeignKey(Supplier, on_delete=models.SET_NULL,null=True)
    date=models.DateField()
    gtotal=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
    def __str__(self):
        return str(self.id)

class Order_items(models.Model):
    order_id=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    item_id=models.ForeignKey(Item,on_delete=models.SET_NULL,null=True)
    quantity_ordered=models.IntegerField()
    purchase_price=models.DecimalField(max_digits=10,decimal_places=2)
    mrp=models.DecimalField(max_digits=10,decimal_places=2)
    batchno=models.CharField(max_length=10,null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    exp_date=models.DateField(null=True)
    def __str__(self):
        return str(self.id)
