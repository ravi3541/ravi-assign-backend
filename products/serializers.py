from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'category', 'tagline', 'description', 'product_code', 'price']


class CheckoutSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    qty = serializers.IntegerField()
