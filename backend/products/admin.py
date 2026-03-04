from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Product, ProductVariant, ProductImage, InventoryLog


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ['name', 'slug', 'parent']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor', 'category', 'price_kes', 'is_active', 'created_at']
    list_filter = ['is_active', 'category', 'vendor']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductVariantInline, ProductImageInline]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['sku', 'product', 'size', 'color', 'stock', 'get_price']
    list_filter = ['product']
    search_fields = ['sku', 'product__name']


@admin.register(InventoryLog)
class InventoryLogAdmin(admin.ModelAdmin):
    list_display = ['product_variant', 'change', 'reason', 'created_at']
    list_filter = ['reason', 'created_at']
    search_fields = ['product_variant__sku', 'note']
    readonly_fields = ['created_at']
