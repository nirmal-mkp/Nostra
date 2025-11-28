from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Cart, CartItem, Products
from django.contrib.auth.decorators import login_required

def home(request):
    products = Products.objects.all()
    return render(request, 'shop/home.html', {"products":products})

def categories(request):
    return render(request, 'shop/categories.html')

def contact(request):
    return render(request, 'shop/contact.html')

def about(request):
    return render(request, 'shop/about.html')

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to homepage or products list
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'shop/cart.html', {'cart': cart})

from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Go to login page after sign up
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

from django.shortcuts import redirect, get_object_or_404

def buy_now(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    # Clear existing cart or create a new cart with this product only
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Optionally clear other items: cart.items.all().delete()
    CartItem.objects.filter(cart=cart).delete()
    
    # Add this item with quantity=1
    CartItem.objects.create(cart=cart, product=product, quantity=1)
    
    # Redirect to checkout/payment page
    return redirect('cart_detail')  # or your checkout URL

import stripe
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# stripe.api_key = settings.STRIPE_SECRET_KEY

# def payment_page(request):
#     return render(request, 'shop/payment.html', {
#         'stripe_public_key': settings.STRIPE_PUBLIC_KEY
#     })

# @csrf_exempt
# def create_payment_intent(request):
#     try:
#         data = json.loads(request.body)
#         amount = int(data['amount'])  # amount in cents

#         intent = stripe.PaymentIntent.create(
#             amount=amount,
#             currency='inr',
#             payment_method_types=['card'],
#         )
#         return JsonResponse({'clientSecret': intent['client_secret']})
#     except Exception as e:
#         return JsonResponse({'error': str(e)})
    
from django.shortcuts import render, redirect
from .paypal import paypalrestsdk

def paypal_payment(request):
    if request.method == 'POST':
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": request.build_absolute_uri('/paypal/execute/'),
                "cancel_url": request.build_absolute_uri('/paypal/cancel/')},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Your Product",
                        "sku": "prod1",
                        "price": "0.01",
                        "currency": "USD",
                        "quantity": 1
                    }]},
                "amount": {
                    "total": "0.01",
                    "currency": "USD"
                },
                "description": "Demo purchase."
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    return redirect(link.href)
        else:
            return render(request, "shop/payment_failed.html", {"error": payment.error})
    return render(request, "shop/payment.html")

import paypalrestsdk
from django.shortcuts import render, redirect

def paypal_execute(request):
    # Get the PayPal payment id and payer id from the GET parameters
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    if not payment_id or not payer_id:
        return render(request, "shop/payment_failed.html", {'error': "Missing paymentId or PayerID."})

    # Find and execute the payment
    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        # You can mark the order as paid here or perform further logic
        return render(request, "shop/payment_success.html")
    else:
        # Optional: Show the error message from PayPal
        error = payment.error if hasattr(payment, 'error') else "Unknown error"
        return render(request, "shop/payment_failed.html", {'error': error})

def paypal_cancel(request):
    # The payment was cancelled by the user
    return render(request, "shop/payment_cancelled.html")
