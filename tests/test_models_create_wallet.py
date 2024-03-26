from unittest import TestCase

from django.contrib.auth.models import User

from wallet.models import Wallet, WalletType, WalletCurrency


class WalletModelRubTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tuser", password="testpass")
        self.wallet_rub = Wallet.objects.create(
            name="TEST0001",
            type=WalletType.VISA.value,
            currency=WalletCurrency.RUBLE.value,
            balance=100.00,
            user=self.user,
        )

    def tearDown(self):
        Wallet.objects.all().delete()
        User.objects.all().delete()

    def test_wallet_rub(self):
        self.assertEqual(self.wallet_rub.name, "TEST0001")
        self.assertEqual(self.wallet_rub.type, WalletType.VISA.value)
        self.assertEqual(self.wallet_rub.currency, WalletCurrency.RUBLE.value)
        self.assertEqual(self.wallet_rub.balance, 100.00)
        self.assertEqual(self.wallet_rub.user, self.user)


class WalletModelEuroTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tuser", password="testpass")
        self.wallet_euro = Wallet.objects.create(
            name="TEST0002",
            type=WalletType.MASTERCARD.value,
            currency=WalletCurrency.EURO.value,
            balance=3.00,
            user=self.user,
        )

    def tearDown(self):
        Wallet.objects.all().delete()
        User.objects.all().delete()

    def test_wallet_euro(self):
        self.assertEqual(self.wallet_euro.name, "TEST0002")
        self.assertEqual(self.wallet_euro.type, WalletType.MASTERCARD.value)
        self.assertEqual(self.wallet_euro.currency, WalletCurrency.EURO.value)
        self.assertEqual(self.wallet_euro.balance, 3.00)
        self.assertEqual(self.wallet_euro.user, self.user)


class WalletModelUsdTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tuser", password="testpass")
        self.wallet_usd = Wallet.objects.create(
            name="TEST0003",
            type=WalletType.VISA.value,
            currency=WalletCurrency.DOLLAR.value,
            balance=3.00,
            user=self.user,
        )

    def tearDown(self):
        Wallet.objects.all().delete()
        User.objects.all().delete()

    def test_wallet_usd(self):
        self.assertEqual(self.wallet_usd.name, "TEST0003")
        self.assertEqual(self.wallet_usd.type, WalletType.VISA.value)
        self.assertEqual(self.wallet_usd.currency, WalletCurrency.DOLLAR.value)
        self.assertEqual(self.wallet_usd.balance, 3.00)
        self.assertEqual(self.wallet_usd.user, self.user)
