from django.contrib.auth.models import User
from django.db import models
from enum import Enum


class WalletCurrency(Enum):
    RUBLE = "RUB"
    DOLLAR = "USD"
    EURO = "EUR"

    @classmethod
    def choices(cls):
        return tuple((c.value, c.value) for c in cls)


class WalletType(Enum):
    VISA = "Visa"
    MASTERCARD = "Mastercard"

    @classmethod
    def choices(cls):
        return tuple((t.value, t.value) for t in cls)


class TransactionStatus(Enum):
    PAID = "PAID"
    FAILED = "FAILED"

    @classmethod
    def choices(cls):
        return tuple((s.value, s.value) for s in cls)


class Wallet(models.Model):
    name = models.CharField(max_length=8, unique=True)
    type = models.CharField(choices=WalletType.choices(), max_length=15)
    currency = models.CharField(choices=WalletCurrency.choices(), max_length=5)
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

    def __str__(self):
        return self.name


class Transaction(models.Model):
    sender = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions_sender")
    receiver = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions_receiver")
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    commission = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(choices=TransactionStatus.choices(), max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)
