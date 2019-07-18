from django import forms
from .models import Stock
class StockForm(forms.ModelForm):
    class Meta:
        model= Stock
        exclude = ['item_id','unit_id']
    exp_date=forms.DateField(label='Expiry Date')

