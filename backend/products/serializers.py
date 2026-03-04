from rest_framework import serializers
from .models import Category, Product, ProductVariant, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary']


class ProductVariantSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductVariant
        fields = ['id', 'sku', 'size', 'color', 'price', 'stock']
    
    def get_price(self, obj):
        return str(obj.get_price())


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price_kes', 'category_name', 'primary_image', 'is_active']
    
    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            return self.context['request'].build_absolute_uri(primary.image.url)
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    vendor_name = serializers.CharField(source='vendor.display_name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price_kes', 'category', 
                  'vendor_name', 'variants', 'images', 'is_active', 'created_at']
