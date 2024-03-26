from django.test import TestCase
from django.contrib.auth.models import User

from wallet.models import (
    Wallet,
    WalletType,
    WalletCurrency,
    Transaction,
    TransactionStatus,
)


class TransactionModelTestCase(TestCase):
    def setUp(self):
        """
        The creation of all types of wallets is necessary for testing transactions
        """

        # wallets for user_1 in all possible currencies and
        # additionally a ruble wallet to verify the transaction to yourself

        self.user_1 = User.objects.create_user(
            username="tuser1", password="testpass"
        )

        self.wallet_rub_1_user_1 = Wallet.objects.create(
            name="RUB0U101",
            type=WalletType.VISA.value,
            currency=WalletCurrency.RUBLE.value,
            balance=100.00,
            user=self.user_1,
        )
        self.wallet_rub_2_user_1 = Wallet.objects.create(
            name="RUB0U102",
            type=WalletType.MASTERCARD.value,
            currency=WalletCurrency.RUBLE.value,
            balance=100.00,
            user=self.user_1,
        )
        self.wallet_eur_user_1 = Wallet.objects.create(
            name="EUR0U101",
            type=WalletType.VISA.value,
            currency=WalletCurrency.EURO.value,
            balance=3.00,
            user=self.user_1,
        )
        self.wallet_usd_user_1 = Wallet.objects.create(
            name="USD0U101",
            type=WalletType.MASTERCARD.value,
            currency=WalletCurrency.DOLLAR.value,
            balance=3.00,
            user=self.user_1,
        )

        # wallets for user_2 in all possible currencies and
        # additionally a EURO wallet to verify the transaction to yourself

        self.user_2 = User.objects.create_user(
            username="tuser2", password="testpass"
        )

        self.wallet_rub_user_2 = Wallet.objects.create(
            name="RUB0U201",
            type=WalletType.VISA.value,
            currency=WalletCurrency.RUBLE.value,
            balance=100.00,
            user=self.user_2,
        )
        self.wallet_eur_1_user_2 = Wallet.objects.create(
            name="EUR0U201",
            type=WalletType.VISA.value,
            currency=WalletCurrency.EURO.value,
            balance=3.00,
            user=self.user_2,
        )
        self.wallet_eur_2_user_2 = Wallet.objects.create(
            name="EUR0U202",
            type=WalletType.VISA.value,
            currency=WalletCurrency.EURO.value,
            balance=3.00,
            user=self.user_2,
        )

        # wallets for user_3 in all possible currencies and
        # additionally a dollar wallet to verify the transaction to yourself

        self.user_3 = User.objects.create_user(
            username="tuser3", password="testpass"
        )

        self.wallet_eur_user_3 = Wallet.objects.create(
            name="EUR0U301",
            type=WalletType.VISA.value,
            currency=WalletCurrency.EURO.value,
            balance=3.00,
            user=self.user_3,
        )
        self.wallet_usd_1_user_3 = Wallet.objects.create(
            name="USD0U301",
            type=WalletType.MASTERCARD.value,
            currency=WalletCurrency.DOLLAR.value,
            balance=3.00,
            user=self.user_3,
        )
        self.wallet_usd_2_user_3 = Wallet.objects.create(
            name="USD0U302",
            type=WalletType.MASTERCARD.value,
            currency=WalletCurrency.DOLLAR.value,
            balance=3.00,
            user=self.user_3,
        )

    def tearDown(self):
        Wallet.objects.all().delete()
        User.objects.all().delete()

    def test_transaction(self):
        transaction_1 = Transaction.objects.create(
            sender=self.wallet_rub_1_user_1,
            receiver=self.wallet_rub_2_user_1,
            amount=50.00,
            commission=0.00,
            status=TransactionStatus.PAID.value,
        )
        self.assertEqual(transaction_1.sender, self.wallet_rub_1_user_1)
        self.assertEqual(transaction_1.receiver, self.wallet_rub_2_user_1)
        self.assertEqual(transaction_1.amount, 50.00)
        self.assertEqual(transaction_1.commission, 0.00)
        self.assertEqual(transaction_1.status, TransactionStatus.PAID.value)

        transaction_2 = Transaction.objects.create(
            sender=self.wallet_rub_2_user_1,
            receiver=self.wallet_rub_user_2,
            amount=100.00,
            commission=10.00,
            status=TransactionStatus.PAID.value,
        )
        self.assertEqual(transaction_2.sender, self.wallet_rub_2_user_1)
        self.assertEqual(transaction_2.receiver, self.wallet_rub_user_2)
        self.assertEqual(transaction_2.amount, 100.00)
        self.assertEqual(transaction_2.commission, 10.00)
        self.assertEqual(transaction_2.status, TransactionStatus.PAID.value)

        transaction_3 = Transaction.objects.create(
            sender=self.wallet_eur_1_user_2,
            receiver=self.wallet_eur_2_user_2,
            amount=1.00,
            commission=0.00,
            status=TransactionStatus.PAID.value,
        )
        self.assertEqual(transaction_3.sender, self.wallet_eur_1_user_2)
        self.assertEqual(transaction_3.receiver, self.wallet_eur_2_user_2)
        self.assertEqual(transaction_3.amount, 1.00)
        self.assertEqual(transaction_3.commission, 0.00)
        self.assertEqual(transaction_3.status, TransactionStatus.PAID.value)

        transaction_4 = Transaction.objects.create(
            sender=self.wallet_eur_2_user_2,
            receiver=self.wallet_eur_user_3,
            amount=1.00,
            commission=0.10,
            status=TransactionStatus.PAID.value,
        )
        self.assertEqual(transaction_4.sender, self.wallet_eur_2_user_2)
        self.assertEqual(transaction_4.receiver, self.wallet_eur_user_3)
        self.assertEqual(transaction_4.amount, 1.00)
        self.assertEqual(transaction_4.commission, 0.10)
        self.assertEqual(transaction_4.status, TransactionStatus.PAID.value)

        transaction_5 = Transaction.objects.create(
            sender=self.wallet_usd_1_user_3,
            receiver=self.wallet_usd_2_user_3,
            amount=1.00,
            commission=0.00,
            status=TransactionStatus.PAID.value,
        )
        self.assertEqual(transaction_5.sender, self.wallet_usd_1_user_3)
        self.assertEqual(transaction_5.receiver, self.wallet_usd_2_user_3)
        self.assertEqual(transaction_5.amount, 1.00)
        self.assertEqual(transaction_5.commission, 0.00)
        self.assertEqual(transaction_5.status, TransactionStatus.PAID.value)

        transaction_6 = Transaction.objects.create(
            sender=self.wallet_usd_2_user_3,
            receiver=self.wallet_usd_user_1,
            amount=1.00,
            commission=0.10,
            status=TransactionStatus.PAID.value,
        )
        self.assertEqual(transaction_6.sender, self.wallet_usd_2_user_3)
        self.assertEqual(transaction_6.receiver, self.wallet_usd_user_1)
        self.assertEqual(transaction_6.amount, 1.00)
        self.assertEqual(transaction_6.commission, 0.10)
        self.assertEqual(transaction_6.status, TransactionStatus.PAID.value)

        transaction_7 = Transaction.objects.create(
            sender=self.wallet_rub_1_user_1,
            receiver=self.wallet_eur_user_1,
            amount=1.00,
            commission=0.00,
            status=TransactionStatus.FAILED.value,
        )
        self.assertEqual(transaction_7.sender, self.wallet_rub_1_user_1)
        self.assertEqual(transaction_7.receiver, self.wallet_eur_user_1)
        self.assertEqual(transaction_7.amount, 1.00)
        self.assertEqual(transaction_7.commission, 0.00)
        self.assertEqual(transaction_7.status, TransactionStatus.FAILED.value)

        transaction_8 = Transaction.objects.create(
            sender=self.wallet_eur_user_3,
            receiver=self.wallet_eur_2_user_2,
            amount=10.00,
            commission=1.00,
            status=TransactionStatus.FAILED.value,
        )
        self.assertEqual(transaction_8.sender, self.wallet_eur_user_3)
        self.assertEqual(transaction_8.receiver, self.wallet_eur_2_user_2)
        self.assertEqual(transaction_8.amount, 10.00)
        self.assertEqual(transaction_8.commission, 1.00)
        self.assertEqual(transaction_8.status, TransactionStatus.FAILED.value)
