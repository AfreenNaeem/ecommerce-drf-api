from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Product

from .models import Category, Product, Cart, CartItem, Order, OrderItem, CustomUser
from .serializers import UserSerializer, CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully"})
    return Response(serializer.errors)


# CREATE + READ
@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


# UPDATE + DELETE
@api_view(['PUT', 'DELETE'])
def category_detail(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    if request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        category.delete()
        return Response({"message": "Deleted successfully"})
    


# CREATE + READ
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


# UPDATE + DELETE
@api_view(['PUT', 'DELETE'])
def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        product.delete()
        return Response({"message": "Deleted successfully"})
    
# ADD TO CART + VIEW CART
@api_view(['GET', 'POST'])
def cart_list(request):
    if request.method == 'GET':
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


# ADD CART ITEM
@api_view(['GET', 'POST'])
def add_to_cart(request):
    if request.method == 'GET':
        items = CartItem.objects.all()
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


# UPDATE + DELETE CART ITEM
@api_view(['PUT', 'DELETE'])
def cart_item_detail(request, id):
    try:
        cart_item = CartItem.objects.get(id=id)
    except CartItem.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    if request.method == 'PUT':
        serializer = CartItemSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        cart_item.delete()
        return Response({"message": "Deleted successfully"})
    
# PLACE ORDER + VIEW ORDERS
@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['GET', 'POST'])
def add_order_item(request):
    if request.method == 'GET':
        order_items = OrderItem.objects.all()
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
def home(request):

    products = Product.objects.all()

    return render(request, 'home.html', {'products': products})
    

class CustomLoginView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):

        response = super().post(request, *args, **kwargs)

        username = request.data.get("username")

        user = CustomUser.objects.get(username=username)

        # only customer
        if user.role == 'customer':

            cart_exists = Cart.objects.filter(user=user).exists()

            if not cart_exists:
                Cart.objects.create(user=user)

        return response
    