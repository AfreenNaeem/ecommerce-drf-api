from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register/', views.register),
    path('login/', views.CustomLoginView.as_view()),
    # Category APIs
    path('categories/', views.category_list),
    path('categories/<int:id>/', views.category_detail),

    path('products/', views.product_list),
    path('products/<int:id>/', views.product_detail),

    path('carts/', views.cart_list),
    path('cart-items/', views.add_to_cart),
    path('cart-items/<int:id>/', views.cart_item_detail),

    path('orders/', views.order_list),
    path('order-items/', views.add_order_item),
]