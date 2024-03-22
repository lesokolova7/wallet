from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from wallet.models import Wallet, Transaction


class SignUpViewTestCase(TestCase):
    def test_sign_up_view_get(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tuser", password="testpass")
        self.client.login(username="tuser", password="testpass")

    def test_home_view_authenticated_user(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/home.html")

    def test_home_view_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)


class CreateWalletViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tuser", password="testpass")
        self.client.login(username="tuser", password="testpass")

    def test_create_wallet_view_get(self):
        response = self.client.get(reverse("create_wallet"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/create_wallet.html")

    def test_create_wallet_view_post(self):
        initial_wallet_count = Wallet.objects.count()
        response = self.client.post(
            reverse("create_wallet"), {"type": "Visa", "currency": "RUB"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Wallet.objects.count(), initial_wallet_count + 1)


class DeleteWalletViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tuser", password="testpass")
        self.client.login(username="tuser", password="testpass")
        self.wallet = Wallet.objects.create(
            name="TEST0001", type="Visa", currency="RUB", balance=100.00, user=self.user
        )

    def test_delete_wallet_view_post(self):
        initial_wallet_count = Wallet.objects.count()
        response = self.client.post(reverse("delete_wallet", args=[self.wallet.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Wallet.objects.count(), initial_wallet_count - 1)


class MakeTransactionViewTestCase(TestCase):
    def setUp(self):
        self.sender_user = User.objects.create_user(
            username="sender", password="testpass"
        )
        self.client.login(username="sender", password="testpass")
        self.sender_wallet = Wallet.objects.create(
            name="TEST000S",
            type="Visa",
            currency="EUR",
            balance=3.00,
            user=self.sender_user,
        )
        self.receiver_user = User.objects.create_user(
            username="receiver", password="testpass"
        )
        self.receiver_wallet = Wallet.objects.create(
            name="TEST000R",
            type="Mastercard",
            currency="EUR",
            balance=3.00,
            user=self.receiver_user,
        )

    def test_make_transaction_view_get(self):
        response = self.client.get(
            reverse("make_transaction", args=[self.sender_wallet.name]), follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_make_transaction_view_post(self):
        initial_transaction_count = Transaction.objects.count()
        url = reverse("make_transaction", args=[self.sender_wallet.name])
        response = self.client.post(
            url, {"receiver": self.receiver_wallet.id, "amount": 1.00}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Transaction.objects.count(), initial_transaction_count + 1)
