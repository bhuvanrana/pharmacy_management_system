from django.db import models

# Create your models here.
class Item(models.Model):
    unit_type = (
        ("tablet", "tablet"),
        ('capsule', 'capsule'),
        ('injection', 'injection'),
        ("pouch", "pouch"),
        ("bottle", "bottle"),
        ("cream", "cream"),
        ("gel", "gel"),
        ('other', 'other'),
    )
    name=models.CharField(max_length=70)
    manufacturer=models.CharField(max_length=70)
    description=models.CharField(max_length=300)
    rackno=models.CharField(max_length=5)
    type = models.CharField(max_length=15, choices=unit_type)
    per_unit = models.IntegerField(null=True)
    min_qty = models.IntegerField(default=5)
    MRP = models.DecimalField(max_digits=10, decimal_places=2)

    total_no_of_units = models.IntegerField(default=0)  # n
    total_loose_qty = models.IntegerField(default=0)
    discount = models.DecimalField(max_digits=4,decimal_places=2,default=1.5)
    def __str__(self):
        return str(self.id)








