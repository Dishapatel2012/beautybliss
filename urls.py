from django.urls import path
from django.contrib import admin
from .import views
from .views import categoryView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm ,MyPasswordChangeForm, MySetPasswordForm
from .views import contact,orders
from .views import return_refund,privacy_policy
# from .views import checkout

urlpatterns = [
path('',views.home, name='home'),
path('about/',views.about, name='about'),
path('contact/',views.contact, name='contact'),
path('face/',views.face, name='face'),
path('body/',views.body, name='body'),
path('hair/',views.hair, name='hair'),
path('invoice/<str:payment_id>/', views.generate_invoice, name='generate_invoice'),
path('makeup/',views.makeup, name='makeup'),
path('return-refund/', return_refund, name='return_refund'),
path('privacy-policy/', privacy_policy, name='privacy_policy'),
path('category/<slug:val>/',views.categoryView.as_view(), name='category'),
path('category-title/<val>/',views.categoryTitle.as_view(), name='category-title'),
path('product-detail/<int:pk>/',views.ProductDetail.as_view(), name='product-detail'),
path('profile/',views.ProfileView.as_view(),name='profile'),
path('address/',views.address,name='address'),
path('add-to-cart/',views.add_to_cart, name="add-to-cart"),
path('cart/',views.show_cart,name="showcart"),
path('checkout/', views.checkout.as_view(), name="checkout"),
path('paymentdone/', views.payment_done, name="paymentdone"),
path('orders/', views.orders, name="orders"),
path('updateAddress/<int:pk>',views.updateAddress.as_view(), name='updateAddress'),

path('registration/',views.CustomerRegistrationView.as_view(), name='customerregistration'),
path('accounts/login/', auth_view.LoginView.as_view(template_name='myapp/login.html',authentication_form=LoginForm),name='login'),

path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name="myapp/changepassword.html",form_class=MyPasswordChangeForm,success_url='/passwordchangedone'),name="passwordchange"),
path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name="myapp/passwordchangedone.html"),name="passwordchangedone"),
path('logout/', views.Logout, name='logout'),

path('search/', views.search, name='search'),
path('wishlist/',views.show_wishlist,name="showwishlist"),

path('pluscart/', views.plus_cart), 
path('minuscart/', views.minus_cart), 
path('removecart/', views.remove_cart),
path('pluswishlist/', views.plus_wishlist), 
path('minuswishlist/', views.minus_wishlist), 



path('password-reset/', auth_view.PasswordResetView.as_view(template_name="myapp/password_reset.html",form_class=MyPasswordResetForm ),name="password_reset"),
path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name="myapp/password_reset_done.html"),name="password_reset_done"),
path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name="myapp/password_reset_confirm.html",form_class=MySetPasswordForm ),name="password_reset_confirm"),
path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name="myapp/password_reset_complete.html"),name="password_reset_complete"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.site_header = "Beauty Bliss"
admin.site.site_title = "Beauty Bliss"
admin.site.site_index_title = "Welcome to Beauty Bliss Website"