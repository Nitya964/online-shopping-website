from rest_framework import serializers
from .models import Product, CustomUser, Cart, Wishlist, Order, OrderItem


from rest_framework_simplejwt.views import (
    TokenObtainPairView,    # Login
    TokenRefreshView,       # Refresh token
)


# ==================== PRODUCT SERIALIZER ====================


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description']




# ==================== USER SERIALIZER ====================


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'gmail', 'phonenumber']




# ==================== CART SERIALIZER ====================


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    total_price = serializers.ReadOnlyField()


    class Meta:
        model = Cart
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price', 'added_at']




# ==================== WISHLIST SERIALIZER ====================


class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)


    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_id', 'added_at']




# ==================== ORDER SERIALIZER ====================


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)


    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'total_price']




class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True, source='order_items')


    class Meta:
        model = Order
        fields = ['id', 'order_date', 'total_amount', 'status', 'tracking_id',
                  'shipping_address', 'phone_number', 'items']
