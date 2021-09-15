from django.db import models

class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("Paid", "Paid"),
        ("Pending", "Pending"),
        ("Cancelled", "Cancelled"),
        ("Delivered", "Delivered"),
    ]
    product = models.TextField(max_length=255, null=False)
    payment_status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS_CHOICES, null=False
    )
