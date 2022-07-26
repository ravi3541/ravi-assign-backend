from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=50)
    tagline = models.CharField(max_length=100)
    description = models.TextField()
    product_code = models.CharField(max_length=15)
    price = models.IntegerField()

    def __str__(self):
        return self.title


