from django.db import models

# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    category = models.CharField(max_length=10) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=10) 
    quantity_within_the_warehouse = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.description}"