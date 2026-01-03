from django.contrib import admin
from core.models import (
    Product, Category, Vendor, CartOrder, CartOrderItems, 
    ProductImages, ProductReview, Wishlist, Address
)

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    # Columns to show in the list
    list_display = ['user', 'title', 'product_image', 'price', 'category', 'vendor', 'featured', 'product_status', 'pid']
    # Efficient searching using the Indexes we created (Rule 5)
    search_fields = ['title', 'category__title', 'vendor__title']
    # Filter options
    list_filter = ['product_status', 'featured', 'in_stock', 'vendor']
    # Rule 6: Least Privilege - Admins can edit status directly from the list, but not sensitive IDs
    list_editable = ['featured', 'product_status'] 
    
    class Media:
        css = {
            'all': ('assets/css/main.css',)
        }

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']
    search_fields = ['title']

class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_image']
    search_fields = ['title']

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']
    list_editable = ['paid_status', 'product_status']
    list_filter = ['paid_status', 'order_date', 'product_status']
    # Rule 2 Support: Orders are critical; we prevent accidental deletion of history here if needed
    # (Django default allows delete, but we track it via logs)

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image', 'qty', 'price', 'total']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']
    list_editable = ['address', 'status']

# Register all models
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)