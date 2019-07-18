from django import forms
from .models import User,Supplier
Role_CHOICES = [
('Admin', 'Admin'),
('Worker','Worker'),
]

class UserForm(forms.ModelForm):
    class Meta:
        model= User
        fields="__all__"
    f_name = forms.CharField(label="First Name",max_length=30)
    l_name = forms.CharField(label="Last Name",max_length=30)
    address=forms.CharField(widget=forms.Textarea)
    email_id = forms.EmailField(required="true")
    phone_no= forms.IntegerField()
    role = forms.CharField(label='Role',widget=forms.RadioSelect(choices=Role_CHOICES),initial="Worker")
    password=forms.CharField(widget=forms.PasswordInput,max_length=70)
    confirm_password = forms.CharField(widget=forms.PasswordInput, max_length=70)

class User_updateForm(forms.ModelForm):
    class Meta:
        model=User
        exclude=['password']
    f_name = forms.CharField(label="First Name", max_length=30)
    l_name = forms.CharField(label="Last Name", max_length=30)
    address = forms.CharField(widget=forms.Textarea)
    email_id = forms.EmailField(required="true")
    phone_no = forms.IntegerField()
    role = forms.CharField(label='Role', widget=forms.RadioSelect(choices=Role_CHOICES))

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"
    address = forms.CharField(widget=forms.Textarea)
    email_id = forms.EmailField(required="true")
    phone_no = forms.IntegerField()