from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES=(
    ('CL','Cleanser'),
    ('SM','Serum'),
    ('FO','Face Oil'),
    ('SS','SunScreen'),
    ('MZ','Moisturizer'),
    ('TR','Toner'),
    ('FM','Face Mask'),
    ('EC','Eye Cream'),
    ('FW','Fash Wash'),
    ('SP','Setting Spray'),
    ('CR','Concealer'),
    ('PM','Primer'),
    ('BW','Body Wash'),
    ('BS','Body Scrub'),
    ('BL','Body Lotion'),
    ('BO','Body Oil'),
    ('BE','Body Serum'),
    ('BG','Body Gel'),
    ('BC','Body Concealer'),
    ('SG','Shower Gel'),
    ('SH','Shampoo'),
    ('CD','Conditioner'),
    ('HM','Hair Mask'),
    ('HC', 'Hair Color'),
    ('HO','Hair Oil'),
    ('HS','Hair Spray'),
    ('DS','Dry Shampoo'),
    ('HD','Hair Detangler'),
    ('HE','Hair Cream'),
    ('HW','Hair Wax'),
    ('PR','Primer'),
    ('FD','Foundation'),
    ('CR','Concealer'),
    ('PR','Powder'),
    ('BU','Blush'),
    ('BZ','Bronzer'),
    ('HG','Highlighter'),
    ('ES','Eye Shadow'),
    ('EL','Eyeliner'),
    ('MS','Mascara'),
    ('LB','Lip Balm'),
    ('LS','Lipstick'),
    ('LG','Lip Gloss'),
    ('SP','Setting Spray'),
    
)

STATE_CHOICES=(
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Uttarakhand','Uttarakhand'),
    ('West Bengal','West Bengal'),
)

STATUS_CHOICES = (
('Accepted','Accepted'),
('Packed','Packed'),
('On The Way','On The Way'),
('Delivered','Delivered'),
('Cancel','Cancel'),
('Pending','Pending'),
)

class Product(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    description = models.TextField()
    composition = models.TextField(default='')
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')
    def __str__(self):
        return self.title

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=100)
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price
    
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name


class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True, null=True)
    paid = models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default="pending")
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default="")

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price



class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)