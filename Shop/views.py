from django.shortcuts import render

def home(request):
    return render(request, 'shop/home.html')

def categories(request):
    return render(request, 'shop/categories.html')

def contact(request):
    return render(request, 'shop/contact.html')

def about(request):
    return render(request, 'shop/about.html')
