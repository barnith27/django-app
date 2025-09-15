from rest_framework import serializers

from .models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'pk', 'name', 'price', 'description', 'discount', 'created_at', 'archived'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = 'delivery_address', 'promocode', 'created_at', 'user', 'products'