from django.urls import path
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

]