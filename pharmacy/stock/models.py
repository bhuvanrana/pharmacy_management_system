from django.db import models
from items.models import Item
# Create your models here.
class Stock(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.SET_NULL,null=True)
    no_of_units = models.IntegerField(default=0)  # n
    loose_qty=models.IntegerField(default=0)
    mrp=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    exp_date = models.DateField()
    batch_no = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id)

    class Meta:
        unique_together = ['item_id', 'batch_no']
