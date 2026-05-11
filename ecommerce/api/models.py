from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.views import TokenObtainPairView



# Custom User
class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('employee', 'Employee'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='customer'
    )

    address = models.TextField(blank=True, null=True)


# Category
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Product
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Cart
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# CartItem
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


# Order
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


# OrderItem
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.product.name
    


class CustomLoginView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):

        response = super().post(request, *args, **kwargs)

        username = request.data.get("username")

        user = CustomUser.objects.get(username=username)

        if user.role == 'customer':

            cart_exists = Cart.objects.filter(user=user).exists()

            if not cart_exists:
                Cart.objects.create(user=user)

        return response