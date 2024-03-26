from django.test import TestCase
from django.contrib.auth.models import User

from wallet.forms import CreateWallet, TransactionForm
from wallet.models import WalletCurrency, Wallet


class CreateWalletFormTestCase(TestCase):

    def setUp(self):
        self.form_completed = CreateWallet(
            data={"type": "Visa", "currency": WalletCurrency.RUBLE.value}
        )
        self.form_empty = CreateWallet(data={})

    def tearDown(self):
        Wallet.objects.all().delete()

    def test_create_wallet_form_valid_data(self):
        self.assertTrue(self.form_completed.is_valid())

    def test_create_wallet_form_invalid_data(self):
        self.assertFalse(self.form_empty.is_valid())
        self.assertEquals(len(self.form_empty.errors), 2)


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
        self.form_valid = TransactionForm(
            sender_currency=WalletCurrency.RUBLE.value,
            sender_id=self.sender_wallet.id,
            data={"receiver": self.receiver_wallet.id, "amount": 50.00},
        )
        self.form_invalid = TransactionForm(
            sender_currency=WalletCurrency.RUBLE.value,
            sender_id=self.sender_wallet.id,
            data={},
        )

    def tearDown(self):
        Wallet.objects.all().delete()
        User.objects.all().delete()

    def test_transaction_form_valid_data(self):
        self.assertTrue(self.form_valid.is_valid())

    def test_transaction_form_invalid_data(self):
        self.assertFalse(self.form_invalid.is_valid())
        self.assertEquals(len(self.form_invalid.errors), 2)
