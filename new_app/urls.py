#new_app/urls.py
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    path('', views.home, name='home'),
    path('product_list/', views.product_list, name='product_list'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:id>/', views.edit_product, name='edit_product'),
    path('delete/<int:id>/', views.delete_product, name='delete_product'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-product/', views.admin_product, name='admin_product'),

 # Cart & Wishlist Actions
    path('cart/', views.cart_view, name='cart_view'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('update_quantity/<int:cart_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    
# Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),

# Admin Order Management
    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('admin-order-detail/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin-update-order/<int:order_id>/', views.admin_update_order, name='admin_update_order'),

# AJAX URLs
    path('add-to-cart-ajax/<int:product_id>/', views.add_to_cart_ajax, name='add_to_cart_ajax'),
    path('add-to-wishlist-ajax/<int:product_id>/', views.add_to_wishlist_ajax, name='add_to_wishlist_ajax'),
    path('remove-from-cart-ajax/<int:cart_id>/', views.remove_from_cart_ajax, name='remove_from_cart_ajax'),
    path('remove-from-wishlist-ajax/<int:wishlist_id>/', views.remove_from_wishlist_ajax, name='remove_from_wishlist_ajax'),
    path('update-cart-quantity-ajax/<int:cart_id>/', views.update_cart_quantity_ajax, name='update_cart_quantity_ajax'),
    
 # ==================== JWT API ENDPOINTS ====================
    # Use these endpoints with Postman to test JWT authentication


    # Auth APIs
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/protected/', views.ProtectedView.as_view(), name='protected'),
    path('api/products/', views.ProductListAPI.as_view(), name='api_product_list'),




    # Product APIs
    path('api/products/add/', views.ProductAddAPI.as_view(), name='api_product_add'),
    path('api/products/<int:product_id>/update/', views.ProductUpdateAPI.as_view(), name='api_product_update'),
    path('api/products/<int:product_id>/delete/', views.ProductDeleteAPI.as_view(), name='api_product_delete'),


    # Cart APIs
    path('api/cart/', views.CartListAPI.as_view(), name='api_cart_list'),
    path('api/cart/add/', views.CartAddAPI.as_view(), name='api_cart_add'),
    path('api/cart/<int:cart_id>/remove/', views.CartRemoveAPI.as_view(), name='api_cart_remove'),
    path('api/cart/<int:cart_id>/update/', views.CartUpdateAPI.as_view(), name='api_cart_update'),


    # Wishlist APIs
    path('api/wishlist/', views.WishlistListAPI.as_view(), name='api_wishlist_list'),
    path('api/wishlist/add/', views.WishlistAddAPI.as_view(), name='api_wishlist_add'),
    path('api/wishlist/<int:wishlist_id>/remove/', views.WishlistRemoveAPI.as_view(), name='api_wishlist_remove'),


    # Order APIs
    path('api/orders/', views.OrderListAPI.as_view(), name='api_order_list'),
    path('api/orders/create/', views.OrderCreateAPI.as_view(), name='api_order_create'),
    path('api/orders/<int:order_id>/', views.OrderDetailAPI.as_view(), name='api_order_detail'),


    # Admin Order APIs
    path('api/admin/orders/', views.AdminOrderListAPI.as_view(), name='api_admin_order_list'),
    path('api/admin/orders/<int:order_id>/update/', views.AdminOrderUpdateAPI.as_view(), name='api_admin_order_update'),
    path('orders/<int:pk>/cancel/', views.cancel_order, name='order_cancel'),
]