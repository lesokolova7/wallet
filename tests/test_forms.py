from django.test import TestCase
from django.contrib.auth.models import User

from wallet.forms import CreateWallet, TransactionForm
from wallet.models import WalletCurrency, Wallet


class CreateWalletFormTestCase(TestCase):
    def test_create_wallet_form_valid_data(self):
        form = CreateWallet(
            data={"type": "Visa", "currency": WalletCurrency.RUBLE.value}
        )
        self.assertTrue(form.is_valid())

    def test_create_wallet_form_invalid_data(self):
        form = CreateWallet(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)


class TransactionFormTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username="test_sender", password="testpass"
        )
        self.receiver = User.objects.create_user(
            username="test_receiver", password="testpass"
        )
        self.sender_wallet = Wallet.objects.create(
            name="SENDER01",
            type="Visa",
            currency=WalletCurrency.RUBLE.value,
            balance=100.00,
            user=self.sender,
        )
        self.receiver_wallet = Wallet.objects.create(
            name="RECEIVER",
            type="Mastercard",
            currency=WalletCurrency.RUBLE.value,
            balance=100.00,
            user=self.receiver,
        )

    def test_transaction_form_valid_data(self):
        form = TransactionForm(
            sender_currency=WalletCurrency.RUBLE.value,
            sender_id=self.sender_wallet.id,
            data={"receiver": self.receiver_wallet.id, "amount": 25.00},
        )
        self.assertTrue(form.is_valid())

    def test_transaction_form_invalid_data(self):
        form = TransactionForm(
            sender_currency=WalletCurrency.RUBLE.value,
            sender_id=self.sender_wallet.id,
            data={},
        )
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)
