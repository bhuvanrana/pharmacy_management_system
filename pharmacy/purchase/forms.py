from django import forms
from django.utils import timezone
from .models import Supply_product,Order_items,Order
class Supply_productForm(forms.ModelForm):
    class Meta:
        model= Supply_product
        exclude = ['item_id','supplier_id']

class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        exclude=['supplier_id']
    date = forms.DateField()
    gtotal = forms.DecimalField(label="Grand Total",max_digits=20, decimal_places=2,required=False)

class Order_itemsForm(forms.ModelForm):
    class Meta:
        model=Order_items
        exclude = ['item_id']

    purchase_price = forms.DecimalField(max_digits=10, decimal_places=2)
    mrp = forms.DecimalField(max_digits=10, decimal_places=2)
    batchno = forms.CharField(label="Batch no",max_length=10,required=False)
    discount = forms.DecimalField(max_digits=5, decimal_places=2,required=False)
    exp_date = forms.DateField(required=False)