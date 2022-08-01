from rest_framework import serializers
from .models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'category', 'tagline', 'description', 'product_code', 'price']


class CheckoutSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    qty = serializers.IntegerField()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
