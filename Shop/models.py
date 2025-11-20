from django.db import models
from django.conf import settings


class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to="products/",null=True,blank=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

# What does it do?
#     The __str__ method returns a string representation of the object.

#     When you use functions like print(product) or view product objects in the Django admin panel, Django calls __str__() to show a human-readable name for each object instead of something generic like <Product object at 0x...>.​

#     For example, if your product is "Bluetooth Speaker", then print(product) will display Bluetooth Speaker.

# Why is it important?
#     It makes working with your model objects in the admin panel and shell much clearer and easier.

#     Without it, Django’s admin and shell would just show a generic or technical name that isn’t helpful.