from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views import View 
from .forms import ContactForm
from .models import Product,Customer,Cart,Payment,OrderPlaced,Wishlist
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.urls import reverse  
from django.db.models import Q
import razorpay
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout

import os
from reportlab.platypus import Table,TableStyle, Image, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors


# Create your views here.
def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user = request.user))
    return render(request, 'myapp/home.html',locals())

def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
      wishitem = len(Wishlist.objects.filter(user = request.user))
    return render(request, 'myapp/about.html',locals())

def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user = request.user))
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save form data
            messages.success(request, "Your message has been sent successfully!")  # Django message framework
            return redirect('contact')  # Reload the page to show the success message
    else:
        form = ContactForm()
    
    return render(request, 'myapp/contact.html', {'form': form})

class categoryView(View):
    def get(self, request, val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
          wishitem = len(Wishlist.objects.filter(user = request.user))
        product = Product.objects.filter(category = val)
        title = Product.objects.filter(category = val).values('title')
        return render(request, 'myapp/category.html',locals())

class categoryTitle(View):
    def get(self, request,val):
        product = Product.objects.filter(title = val)
        title = Product.objects.filter(category = product[0].category).values('title')
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
          wishitem = len(Wishlist.objects.filter(user = request.user))
        return render(request, 'myapp/category.html',locals())

@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
          wishitem = len(Wishlist.objects.filter(user = request.user))
        return render(request, 'myapp/productdetail.html',locals())

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
          wishitem = len(Wishlist.objects.filter(user = request.user))
        return render(request, "myapp/customerregistrationform.html",locals())

    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! USer Register Successfuly")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, "myapp/customerregistrationform.html",locals())

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
          wishitem = len(Wishlist.objects.filter(user = request.user))
        return render(request, 'myapp/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! profile save successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'myapp/profile.html',locals())

@login_required
def add_to_cart(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user = request.user))
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.selling_price
        amount = amount + value
        totalamount = amount + 00
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
          wishitem = len(Wishlist.objects.filter(user = request.user))
    return render(request,"myapp/addtocart.html",locals())

def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user = request.user))
    product = Wishlist.objects.filter
    return render(request, 'myapp/wishlist.html',locals())

@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self,request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
          wishitem = len(Wishlist.objects.filter(user = request.user))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value= p.quantity * p.product.selling_price
            famount= famount + value
        totalamount = famount + 00    
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency":"INR","receipt":"order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        # {'amount': 109900, 'amount_due': 109900, 'amount_paid': 0, 'attempts': 0, 'created_at': 1740231983, 'currency': 'INR', 'entity': 'order', 'id': 'order_PymHBL9Ww4QhQn', 'notes': [], 'offer_id': None, 'receipt': 'order_rcptid_12', 'status': 'created'}
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user = user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
        return render(request, 'myapp/checkout.html',locals())

@login_required
def payment_done(request):
    order_id=request.GET.get('order_id') 
    payment_id=request.GET.get('payment_id') 
    cust_id=request.GET.get('cust_id') 
    #print("payment_done : oid = ",order_id," pid = ",payment_id," cid = ",cust_id)
    user=request.user 
    # return redirect("orders")
    customer=Customer.objects.get(id=cust_id)
    #To update payment status and payment id
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    #To save order details
    cart=Cart.objects.filter(user=user) 
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect("/orders")

@login_required
def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user = request.user))
    # totalitem = 0
    # wishitem=0
    # if request.user.is_authenticated:
    #     totalitem = len(Cart.objects.filter(user=request.user))
    #     wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user) 
    return render(request, 'myapp/orders.html',locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.selling_price
            amount = amount + value
        totalamount = amount + 00
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.selling_price
            amount = amount + value
        totalamount = amount + 00
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get("prod_id")
        if prod_id:
            cart_item = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()  # Fetch the first entry
            if cart_item:
                cart_item.delete()  # Delete only one entry
                
                # Recalculate cart totals
                total_amount = sum(item.product.selling_price * item.quantity for item in Cart.objects.filter(user=request.user))
                
                return JsonResponse({"amount": 0, "totalamount": total_amount})  
            else:
                return JsonResponse({"error": "Item not found in cart"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)

def plus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data={
            'message':'Wishlist Added Successfully',
        }
        return JsonResponse(data)

def minus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data={
            'message':'Wishlist Remove Successfully',
        }
        return JsonResponse(data)

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user = request.user))
    return render(request, 'myapp/address.html',locals())

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
          wishitem = len(Wishlist.objects.filter(user = request.user))
        return render(request, 'myapp/updateAddress.html',locals())


    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! profile update successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")

def Logout(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS,'Successfully Loged Out...')
    return redirect(reverse('home'))
        
def face(request):
    return render(request, 'myapp/face.html')

def body(request):
    return render(request, 'myapp/body.html')

def hair(request):
    return render(request, 'myapp/hair.html')

def makeup(request):
    return render(request, 'myapp/makeup.html')

def return_refund(request):
    return render(request, 'myapp/return_refund.html')

def privacy_policy(request):
    return render(request, 'myapp/privacy_policy.html')

def search(request):
    query = request.GET.get('search', '') 
    totalitem = 0
    wishitem = 0

    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
        wishitem = Wishlist.objects.filter(user=request.user).count()

    product = Product.objects.filter(Q(title__icontains=query)) if query else Product.objects.none()

    return render(request, "myapp/search.html", {"product": product, "totalitem": totalitem, "wishitem": wishitem})


def generate_invoice(request, payment_id):
    payment = get_object_or_404(Payment, razorpay_payment_id=payment_id)
    orders = OrderPlaced.objects.filter(payment=payment)
    
    if not orders.exists():
        return HttpResponse("No orders found for this payment.", content_type="text/plain")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{payment_id}.pdf"'
    
    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Invoice Title
    title = Paragraph("<b><font size=18>Beauty Bliss Invoice</font></b>", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Invoice Details
    details = [
        ["Invoice ID:", str(payment.id)],
        ["Payment ID:", payment.razorpay_payment_id],
        ["Order ID:", payment.razorpay_order_id],
        ["Customer:", orders.first().customer.name],
        ["Address:", f"{orders.first().customer.city} - {orders.first().customer.zipcode}"],
        ["Mobile:", orders.first().customer.mobile],
    ]

    # Table for Invoice Details
    detail_table = Table(details, colWidths=[100, 300])
    detail_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    elements.append(detail_table)
    elements.append(Spacer(1, 20))

    # Product Table
    data = [["Product Image", "Name", "Price", "QTY", "Amount"]]
    total_amount = 0

    for order in orders:
        product_image = getattr(order.product, 'product_image', None)
        img_path = os.path.join(settings.MEDIA_ROOT, str(product_image)) if product_image else None
        
        if img_path and os.path.exists(img_path):
            img = Image(img_path, width=50, height=50)
        else:
            img = Paragraph("No Image", styles["Normal"])

        data.append([
            img,
            Paragraph(order.product.title, styles["Normal"]),
            f"Rs.{order.total_cost}",
            str(order.quantity),
            f"Rs.{order.total_cost*order.quantity}"
            
        ])

        total_amount += (order.total_cost*order.quantity)

    # Tax & Grand Total
    data.append(["", "", "", "Grand Total", f"Rs.{total_amount}"])

    # Define Table Style
    table = Table(data, colWidths=[80, 150, 80, 70, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # Notes Section (FIXED)
    # Build PDF
    pdf.build(elements)
    
    return response