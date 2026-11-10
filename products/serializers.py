from rest_framework import serializers
from .models import Product, Category
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count']

    def get_product_count(self, obj):
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product

        fields = [
            'id',
            'name',
            'price',
            'stock',
            'is_available',
            'created_at',
            'image',
            'category',
            'category_id',
            'created_by',
        ]