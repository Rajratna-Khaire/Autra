from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth import get_user_model

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Trade(models.Model):
    ACTION_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]

    TRADE_TYPE_CHOICES = [
        ('MANUAL', 'Manual'),
        ('AUTO', 'Auto'),
    ]

    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=10)
    action = models.CharField(max_length=4, choices=ACTION_CHOICES)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sl = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Stop Loss
    target = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Target Price
    trade_type = models.CharField(max_length=10, choices=TRADE_TYPE_CHOICES, default='AUTO')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='COMPLETED')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.action} {self.quantity}x {self.stock_symbol} @ {self.price}"

