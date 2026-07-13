from django.db import models

#create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100, blank=True)
    gmail = models.EmailField(blank=True)
    phonenumber = models.CharField(max_length=15, blank=True)

    def __str__(self):
            return self.username

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name} (Qty: {self.quantity})"

    @property
    def total_price(self):
        return self.quantity * self.product.price

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')


    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]


    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='Cash on Delivery')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    tracking_id = models.CharField(max_length=100, blank=True, null=True)
    tracking_details = models.TextField(blank=True, null=True)
    shipping_address = models.TextField()
    phone_number = models.CharField(max_length=15)


    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


    @property
    def items_count(self):
        return self.order_items.count()

        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of order


    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


    @property
    def total_price(self):
        return self.quantity * self.price

