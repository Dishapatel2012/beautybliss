from django.contrib import admin
from .models import ContactMessage
from .models import Product,Customer,Cart,Payment,OrderPlaced,Wishlist
from django.contrib.auth.models import Group

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    List_display = ['id','title','Selling_price','description','composition','category','product_image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    List_display = ['id','user','locality','city','state','zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    List_display = ['id','user','product','quantity']
    
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone',)  # Show fields in admin panel
    search_fields = ('name', 'email', 'phone')  # Enable search functional

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status','payment']

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product']

admin.site.unregister(Group)
