from django.contrib.auth.models import User
from django.db import models
from dataclasses import dataclass


@dataclass
class WalletCurrency:
    ruble = "RUB"
    dollar = "USD"
    euro = "EUR"


class WalletUser(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, unique=True)
    name = models.TextField()


class Wallet(models.Model):
    WALLET_TYPE_CHOICES = [
        ("Visa", "Visa"),
        ("Mastercard", "Mastercard")
    ]

    WALLET_CURRENCY_CHOICES = [
        (WalletCurrency.ruble, WalletCurrency.ruble),
        (WalletCurrency.dollar, WalletCurrency.dollar),
        (WalletCurrency.euro, WalletCurrency.euro)
    ]

    name = models.CharField(max_length=8, unique=True)
    type = models.TextField(choices=WALLET_TYPE_CHOICES)
    currency = models.TextField(choices=WALLET_CURRENCY_CHOICES)
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(WalletUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    sender = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="wallet_of_sender")
    receiver = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="wallet_of_receiver")
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    commission = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

