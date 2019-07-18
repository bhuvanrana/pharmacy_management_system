from django.db import models

# Create your models here.
mode_choices = (
	("Admin", "Admin"),
	("Worker", "Worker"),
)
class User(models.Model):
    f_name=models.CharField(max_length=30)
    l_name = models.CharField(max_length=30)
    address=models.CharField(max_length=150)
    email_id=models.EmailField(max_length=50)
    phone_no=models.CharField(max_length=10)
    username=models.CharField(max_length=50,unique=True,null=True)
    password = models.CharField(max_length=70)
    role = models.CharField(max_length=10, choices=mode_choices, default='Worker')
    def __str__(self):
        return self.f_name+' '+ self.l_name
    #def create(f_n,l_n,add,mail,ph,pwd,role):
       # self.

class Supplier(models.Model):
    name = models.CharField(max_length=100,null=True)
    address = models.CharField(max_length=150)
    email_id = models.EmailField(max_length=50)
    phone_no = models.CharField(max_length=10)
    def __str__(self):
        return self.name