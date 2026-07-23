from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Cart, CustomUser, OrderItem, Product, Wishlist
from .models import Product, CustomUser, Cart, Wishlist, Order, OrderItem
from .models import CustomUser
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Order

# create your views here.
def home(request):
  return render(request, 'home.html')
  


# REGISTER VIEW
def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        name = request.POST.get('name')
        gmail = request.POST.get('gmail')
        phonenumber = request.POST.get('phonenumber')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if password != password_confirm:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})       
        user = CustomUser.objects.create_user(
            username=username,
            name=name,
            gmail=gmail,
            password=password,
            phonenumber=phonenumber
        )
        login(request, user)
        return redirect('home')

    return render(request, 'register.html')

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')
# LOGIN VIEW
def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


# LOGOUT VIEW
def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def admin_product(request):
    if not request.user.is_superuser:
        return redirect('home')
    products = Product.objects.all()
    return render(request, 'admin_products.html', {'products': products})

    # ADMIN - CREATE Product
@login_required
def add_product(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        Product.objects.create(
            name=name,
            price=price,
            description=description
        )
        return redirect('admin_product')
    return render(request, 'add_product.html')

# ADMIN - UPDATE Product
@login_required
def edit_product(request, id):
    if not request.user.is_superuser:
        return redirect('home')
    product = Product.objects.get(id=id)
    if request.method == "POST":
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.save()
        return redirect('admin_product')
    return render(request, 'edit_product.html', {'product': product})

# ADMIN - DELETE Product
@login_required
def delete_product(request, id):
    if not request.user.is_superuser:
        return redirect('home')
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('admin_product')

# USER PRODUCT LIST - Users can view products
@login_required
def product_list(request):
    products = Product.objects.all()
    cart_count = Cart.objects.filter(user=request.user).count()
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    context = {
        'products': products,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count
    }
    return render(request, 'product_list.html', context)

# USER - Add to Cart
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    Cart.objects.get_or_create(user=request.user, product=product)
    return redirect('product_list')


# USER - Remove from Cart
@login_required
def remove_from_cart(request, cart_id):
    cart_item = Cart.objects.get(id=cart_id)
    cart_item.delete()
    return redirect('cart_view')


# USER - View Cart
@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


# USER - Add to Wishlist
@login_required
def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('product_list')


# USER - Remove from Wishlist
@login_required
def remove_from_wishlist(request, wishlist_id):
    wishlist_item = Wishlist.objects.get(id=wishlist_id)
    wishlist_item.delete()
    return redirect('wishlist_view')


# USER - View Wishlist
@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

    # USER - Update Cart Quantity
@login_required
def update_cart_quantity(request, cart_id):
    if request.method == "POST":
        cart_item = Cart.objects.get(id=cart_id, user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart_view')


def add_to_cart(request, product_id):
    user=request.user
    if user.is_authenticated:
        product = Product.objects.get(id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('product_list')
    else:
        return redirect('login')




# USER - View Cart
@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

# USER - Checkout
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items:
        return redirect('product_list')

    total_amount = sum(item.total_price for item in cart_items)

    if request.method == "POST":
        shipping_address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')

        if not shipping_address or not phone_number:
            return render(request, 'checkout.html', {
                'cart_items': cart_items,
                'total_amount': total_amount,
                'error': 'Please provide all required fields'
            })

        # Create Order
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            payment_method='Cash on Delivery',
            shipping_address=shipping_address,
            phone_number=phone_number
        )
        # Create Order Items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        # Clear Cart
        cart_items.delete()

        return redirect('order_success', order_id=order.id)

    # ✅ THIS WAS MISSING (GET request handler)
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'user': request.user
    })


# USER - Order Success
@login_required
def order_success(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    order_items = order.order_items.all()
    return render(request, 'order_success.html', {
        'order': order,
        'order_items': order_items
    })


# USER - My Orders
@login_required
def my_orders(request):
    order = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'my_orders.html', {'orders': order})


# USER - Order Detail
@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    order_items = order.order_items.all()
    return render(request, 'order_detail.html', {
        'order': order,
        'order_items': order_items
    })

# ==================== ORDER MANAGEMENT VIEWS BY ADMIN ====================


# ADMIN - All Orders
@login_required
def admin_orders(request):
    if not request.user.is_superuser:
        return redirect('home')
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'admin_orders.html', {'orders': orders})


# ADMIN - Order Detail
@login_required
def admin_order_detail(request, order_id):
    if not request.user.is_superuser:
        return redirect('home')
    order = Order.objects.get(id=order_id)
    order_items = order.order_items.all()
    return render(request, 'admin_order_detail.html', {
        'order': order,
        'order_items': order_items
    })


# ADMIN - Update Order Status & Tracking
@login_required
def admin_update_order(request, order_id):
    if not request.user.is_superuser:
        return redirect('home')
    order = Order.objects.get(id=order_id)


    if request.method == "POST":
        order.status = request.POST.get('status')
        order.tracking_id = request.POST.get('tracking_id', '')
        order.tracking_details = request.POST.get('tracking_details', '')
        order.save()
        return redirect('admin_order_detail', order_id=order.id)


    return render(request, 'admin_update_order.html', {'order': order})

from django.http import JsonResponse


# ==================== AJAX VIEWS ====================


# AJAX - Add to Cart
@login_required
def add_to_cart_ajax(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Please login to add items to cart'}, status=401)


    try:
        product = Product.objects.get(id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()


        cart_count = Cart.objects.filter(user=request.user).count()
        return JsonResponse({
            'status': 'success',
            'message': 'Added to Cart successfully!',
            'cart_count': cart_count
        })
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)




# AJAX - Add to Wishlist
@login_required
def add_to_wishlist_ajax(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Please login to add items to wishlist'}, status=401)


    try:
        product = Product.objects.get(id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)


        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        if created:
            return JsonResponse({
                'status': 'success',
                'message': 'Added to Wishlist successfully!',
                'wishlist_count': wishlist_count
            })
        else:
            return JsonResponse({
                'status': 'success',
                'message': 'Already in Wishlist!',
                'wishlist_count': wishlist_count
            })
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)




# AJAX - Remove from Cart
@login_required
def remove_from_cart_ajax(request, cart_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Please login first'}, status=401)


    try:
        cart_item = Cart.objects.get(id=cart_id, user=request.user)
        cart_item.delete()


        cart_count = Cart.objects.filter(user=request.user).count()
        cart_items = Cart.objects.filter(user=request.user)
        total = sum(item.total_price for item in cart_items)


        return JsonResponse({
            'status': 'success',
            'message': 'Item removed from cart!',
            'cart_count': cart_count,
            'total': total
        })
    except Cart.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Cart item not found'}, status=404)




# AJAX - Remove from Wishlist
@login_required
def remove_from_wishlist_ajax(request, wishlist_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Please login first'}, status=401)


    try:
        wishlist_item = Wishlist.objects.get(id=wishlist_id, user=request.user)
        wishlist_item.delete()


        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        return JsonResponse({
            'status': 'success',
            'message': 'Item removed from wishlist!',
            'wishlist_count': wishlist_count
        })
    except Wishlist.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Wishlist item not found'}, status=404)

# AJAX - Update Cart Quantity
@login_required
def update_cart_quantity_ajax(request, cart_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Please login first'}, status=401)


    try:
        cart_item = Cart.objects.get(id=cart_id, user=request.user)
        quantity = int(request.POST.get('quantity', 1))


        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save(update_fields=['quantity'])  # Explicitly save only quantity field
        else:
            cart_item.delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Item removed from cart!',
                'item_total': 0,
                'total': sum(item.total_price for item in Cart.objects.filter(user=request.user))
            })


        # Refresh from DB to ensure we have latest data
        cart_item.refresh_from_db()
        cart_items = Cart.objects.filter(user=request.user)
        total = sum(item.total_price for item in cart_items)


        return JsonResponse({
            'status': 'success',
            'message': 'Quantity updated!',
            'item_total': cart_item.total_price,
            'total': total,
            'quantity': cart_item.quantity  # Return the saved quantity for verification
        })
    except Cart.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Cart item not found'}, status=404)
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid quantity'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# ==================== JWT API VIEWS ====================
# REST Framework Imports for JWT
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, UserSerializer, CartSerializer, WishlistSerializer, OrderSerializer


class ProtectedView(APIView):
    """Test view to verify JWT authentication works"""
    permission_classes = [IsAuthenticated]


    def get(self, request):
        return Response({
            'message': 'JWT Authentication successful!',
            'user': request.user.username,
            'user_id': request.user.id,
            'email': request.user.email
        })




# ==================== PRODUCT API VIEWS ====================


class ProductListAPI(APIView):
    """GET all products - No authentication required"""
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({
            'status': 'success',
            'count': products.count(),
            'data': serializer.data
        })




class ProductAddAPI(APIView):
    """POST add product - Admin only"""
    permission_classes = [IsAuthenticated, IsAdminUser]


    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Product added successfully!',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)




class ProductUpdateAPI(APIView):
    """PUT update product - Admin only"""
    permission_classes = [IsAuthenticated, IsAdminUser]


    def put(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'Product updated successfully!',
                    'data': serializer.data
                })
            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)




class ProductDeleteAPI(APIView):
    """DELETE product - Admin only"""
    permission_classes = [IsAuthenticated, IsAdminUser]


    def delete(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return Response({
                'status': 'success',
                'message': 'Product deleted successfully!'
            })
        except Product.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)




# ==================== CART API VIEWS ====================


class CartListAPI(APIView):
    """GET user's cart"""
    permission_classes = [IsAuthenticated]


    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        total = sum(item.total_price for item in cart_items)
        return Response({
            'status': 'success',
            'count': cart_items.count(),
            'total': total,
            'data': serializer.data
        })




class CartAddAPI(APIView):
    """POST add product to cart"""
    permission_classes = [IsAuthenticated]


    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)


        try:
            product = Product.objects.get(id=product_id)
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()


            serializer = CartSerializer(cart_item)
            cart_count = Cart.objects.filter(user=request.user).count()
            return Response({
                'status': 'success',
                'message': 'Added to cart successfully!',
                'cart_count': cart_count,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)




class CartRemoveAPI(APIView):
    """DELETE item from cart"""
    permission_classes = [IsAuthenticated]


    def delete(self, request, cart_id):
        try:
            cart_item = Cart.objects.get(id=cart_id, user=request.user)
            cart_item.delete()
            cart_count = Cart.objects.filter(user=request.user).count()
            return Response({
                'status': 'success',
                'message': 'Item removed from cart!',
                'cart_count': cart_count
            })
        except Cart.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Cart item not found'
            }, status=status.HTTP_404_NOT_FOUND)




class CartUpdateAPI(APIView):
    """PUT update cart item quantity"""
    permission_classes = [IsAuthenticated]


    def put(self, request, cart_id):
        quantity = request.data.get('quantity')
        try:
            cart_item = Cart.objects.get(id=cart_id, user=request.user)
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
                serializer = CartSerializer(cart_item)
                return Response({
                    'status': 'success',
                    'message': 'Quantity updated!',
                    'data': serializer.data
                })
            else:
                cart_item.delete()
                return Response({
                    'status': 'success',
                    'message': 'Item removed from cart!'
                })
        except Cart.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Cart item not found'
            }, status=status.HTTP_404_NOT_FOUND)




# ==================== WISHLIST API VIEWS ====================


class WishlistListAPI(APIView):
    """GET user's wishlist"""
    permission_classes = [IsAuthenticated]


    def get(self, request):
        wishlist_items = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist_items, many=True)
        return Response({
            'status': 'success',
            'count': wishlist_items.count(),
            'data': serializer.data
        })




class WishlistAddAPI(APIView):
    """POST add product to wishlist"""
    permission_classes = [IsAuthenticated]


    def post(self, request):
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=request.user,
                product=product
            )
            serializer = WishlistSerializer(wishlist_item)
            if created:
                return Response({
                    'status': 'success',
                    'message': 'Added to wishlist!',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'status': 'success',
                    'message': 'Already in wishlist!',
                    'data': serializer.data
                })
        except Product.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)




class WishlistRemoveAPI(APIView):
    """DELETE item from wishlist"""
    permission_classes = [IsAuthenticated]


    def delete(self, request, wishlist_id):
        try:
            wishlist_item = Wishlist.objects.get(id=wishlist_id, user=request.user)
            wishlist_item.delete()
            return Response({
                'status': 'success',
                'message': 'Item removed from wishlist!'
            })
        except Wishlist.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Wishlist item not found'
            }, status=status.HTTP_404_NOT_FOUND)




# ==================== ORDER API VIEWS ====================


class OrderListAPI(APIView):
    """GET user's orders"""
    permission_classes = [IsAuthenticated]


    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-order_date')
        serializer = OrderSerializer(orders, many=True)
        return Response({
            'status': 'success',
            'count': orders.count(),
            'data': serializer.data
        })




class OrderDetailAPI(APIView):
    """GET order details"""
    permission_classes = [IsAuthenticated]


    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            serializer = OrderSerializer(order)
            return Response({
                'status': 'success',
                'data': serializer.data
            })
        except Order.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Order not found'
            }, status=status.HTTP_404_NOT_FOUND)




class OrderCreateAPI(APIView):
    """POST create order from cart"""
    permission_classes = [IsAuthenticated]


    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            return Response({
                'status': 'error',
                'message': 'Cart is empty!'
            }, status=status.HTTP_400_BAD_REQUEST)


        shipping_address = request.data.get('shipping_address')
        phone_number = request.data.get('phone_number')


        if not shipping_address or not phone_number:
            return Response({
                'status': 'error',
                'message': 'Please provide shipping address and phone number!'
            }, status=status.HTTP_400_BAD_REQUEST)


        total_amount = sum(item.total_price for item in cart_items)


        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            shipping_address=shipping_address,
            phone_number=phone_number
        )


        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )


        cart_items.delete()


        serializer = OrderSerializer(order)
        return Response({
            'status': 'success',
            'message': 'Order placed successfully!',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)




# ==================== ADMIN ORDER API VIEWS ====================


class AdminOrderListAPI(APIView):
    """GET all orders - Admin only"""
    permission_classes = [IsAuthenticated, IsAdminUser]


    def get(self, request):
        orders = Order.objects.all().order_by('-order_date')
        serializer = OrderSerializer(orders, many=True)
        return Response({
            'status': 'success',
            'count': orders.count(),
            'data': serializer.data
        })




class AdminOrderUpdateAPI(APIView):
    """PUT update order status - Admin only"""
    permission_classes = [IsAuthenticated, IsAdminUser]


    def put(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            order.status = request.data.get('status', order.status)
            order.tracking_id = request.data.get('tracking_id', order.tracking_id)
            order.tracking_details = request.data.get('tracking_details', order.tracking_details)
            order.save()
            serializer = OrderSerializer(order)
            return Response({
                'status': 'success',
                'message': 'Order updated successfully!',
                'data': serializer.data
            })
        except Order.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Order not found'
            }, status=status.HTTP_404_NOT_FOUND)



# Cancel Order
@login_required
@require_POST
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.cancel():
        messages.success(request, "Order cancelled.")
    else:
        messages.error(request, "Cannot cancel this order.")
    # redirect back to order detail or referer
    return redirect(request.META.get('HTTP_REFERER') or 'order_detail', pk=order.pk)
