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


class Order(models.Model):
    status = (
        ('completed', 'completed'),
        ('pending', 'pending'),
        ('cancelled', 'cancelled')
    )

    email = models.EmailField()
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30)
    addr_line1 = models.CharField(max_length=100)
    addr_line2 = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    unit_price = models.IntegerField()
    ordered_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=10, choices=status)



