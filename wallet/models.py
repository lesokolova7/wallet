from django.contrib.auth.models import User
from django.db import models
from enum import Enum


class WalletCurrency(Enum):
    ruble = "RUB"
    dollar = "USD"
    euro = "EUR"

    @classmethod
    def choices(cls):
        return tuple((c.value, c.value) for c in cls)

    def __str__(self):
        return self.value


class WalletType(Enum):
    visa = "Visa"
    mastercard = "Mastercard"

    @classmethod
    def choices(cls):
        return tuple((t.value, t.value) for t in cls)


class TransactionStatus(Enum):
    paid = "PAID"
    failed = "FAILED"


class Wallet(models.Model):
    DoesNotExist = None
    name = models.CharField(max_length=8, unique=True)
    type = models.CharField(choices=WalletType.choices())
    currency = models.CharField(choices=WalletCurrency.choices())
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

    def __str__(self):
        return self.name


class Transaction(models.Model):
    sender = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    receiver = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    commission = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(TransactionStatus)
    timestamp = models.DateTimeField(auto_now_add=True)
