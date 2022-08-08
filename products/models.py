from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False, unique=True)
    category = models.CharField(max_length=50, null=False, blank=False)
    tagline = models.CharField(max_length=100, null=False, blank=False, unique=True)
    description = models.TextField()
    product_code = models.CharField(max_length=15, null=False, blank=False, unique=True)
    price = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.title


class Order(models.Model):
    status = (
        ('completed', 'completed'),
        ('pending', 'pending'),
        ('cancelled', 'cancelled')
    )

    customer_email = models.EmailField(max_length=255, null=False, blank=False)
    customer_name = models.CharField(max_length=50, null=False, blank=False)
    customer_country = models.CharField(max_length=30, null=False, blank=False)
    customer_state = models.CharField(max_length=30, null=True, blank=True)
    customer_city = models.CharField(max_length=30, null=False, blank=False)
    customer_addr_line1 = models.CharField(max_length=100, null=False, blank=False)
    customer_addr_line2 = models.CharField(max_length=100, null=False, blank=False)
    customer_postal_code = models.CharField(max_length=10, null=False, blank=False)
    qty = models.IntegerField(null=False, blank=False)
    unit_price = models.IntegerField(null=False, blank=False)
    ordered_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=10, choices=status)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)



