from django import forms
from .models import Item

unit_type = (
    ("tablet", "tablet"),
    ('capsule', 'capsule'),
    ('injection', 'injection'),
    ("pouch", "pouch"),
    ("bottle", "bottle"),
    ("cream","cream"),
    ("gel","gel"),
    ('other', 'other'),
)


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude=['total_no_of_units','total_loose_qty']
    rackno = forms.CharField(label="Rack Number",max_length=5)
    type= forms.CharField(widget=forms.Select(choices=unit_type))
    per_unit = forms.IntegerField(label='Qty per unit')
    min_qty = forms.IntegerField(label="Minimum Qty")




