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
