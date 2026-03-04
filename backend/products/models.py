from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from common.models import TimeStampedModel


class Category(MPTTModel, TimeStampedModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    class MPTTMeta:
        order_insertion_by = ['name']
    
    class Meta:
        db_table = 'products_category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(TimeStampedModel):
    vendor = models.ForeignKey('vendors.Vendor', on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    price_kes = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'products_product'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductVariant(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=100, unique=True)
    size = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)
    price_kes = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'products_productvariant'
    
    def __str__(self):
        return f"{self.product.name} - {self.sku}"
    
    def get_price(self):
        """Return variant price or fall back to product price"""
        return self.price_kes if self.price_kes else self.product.price_kes


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'products_productimage'
    
    def __str__(self):
        return f"Image for {self.product.name}"
    
    def save(self, *args, **kwargs):
        # Ensure only one primary image per product
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)


class InventoryLog(TimeStampedModel):
    REASON_CHOICES = [
        ('SALE', 'Sale'),
        ('RESTOCK', 'Restock'),
        ('MANUAL_ADJUST', 'Manual Adjustment'),
        ('RETURN', 'Return'),
    ]
    
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='inventory_logs')
    change = models.IntegerField(help_text="Positive for increase, negative for decrease")
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    note = models.TextField(blank=True)
    
    class Meta:
        db_table = 'products_inventorylog'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product_variant.sku}: {self.change} ({self.reason})"
