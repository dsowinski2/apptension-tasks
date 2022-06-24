from django.db import models
from users.models import User


class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("paid", "paid"),
        ("pending", "pending"),
        ("cancelled", "cancelled"),
        ("delivered", "delivered"),
    ]
    product = models.TextField(max_length=255, null=False)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    email = models.TextField(max_length=255, null=False)
    payment_status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS_CHOICES, null=False
    )
    amount_total = models.IntegerField(null=True)
