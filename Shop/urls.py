from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path("", views.home, name = "home"),
    path("categories/", views.categories,  name = "categories"),
    path("contact/", views.contact,  name = "contact"),
    path("about/", views.about,  name = "about"),
    path("add-product/", views.add_product, name="add_product"),
    path("cart/", views.cart_detail, name = "cart_detail"),
    path("add-to-cart/<int:product_id>", views.add_to_cart, name = "add_to_cart"),
    path("signup/", views.signup, name = "signup"),
    # Login
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # Logout  
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    # Signup (custom view)
    path('accounts/signup/', views.signup, name='signup'),
    
    # path('payment/', views.payment_page, name='payment'),
    # path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('payment/', views.paypal_payment, name='paypal_payment'),
    path('paypal/execute/', views.paypal_execute, name='paypal_execute'),
    path('paypal/cancel/', views.paypal_cancel, name='paypal_cancel'),
    path('paypal/payment/<int:product_id>/', views.paypal_payment, name='paypal_payment'),

]