from django.test import TestCase
from django.urls import reverse, resolve

from wallet.views import (
    home,
    sign_up,
    delete_wallet,
    create_wallet,
    make_transaction,
    transaction_success,
    transaction_failed,
)


class WalletURLTests(TestCase):
    def test_home_url_resolves_home_view(self):
        url = reverse("home")
        self.assertEqual(resolve(url).func, home)

    def test_signup_url_resolves_signup_view(self):
        url = reverse("signup")
        self.assertEqual(resolve(url).func, sign_up)

    def test_delete_wallet_url_resolves_delete_wallet_view(self):
        url = reverse("delete_wallet", args=[1])
        self.assertEqual(resolve(url).func, delete_wallet)

    def test_create_wallet_url_resolves_create_wallet_view(self):
        url = reverse("create_wallet")
        self.assertEqual(resolve(url).func, create_wallet)

    def test_make_transaction_url_resolves_make_transaction_view(self):
        url = reverse("make_transaction", args=["wallet_name"])
        self.assertEqual(resolve(url).func, make_transaction)

    def test_transaction_success_url_resolves_transaction_success_view(self):
        url = reverse("transaction_success")
        self.assertEqual(resolve(url).func, transaction_success)

    def test_transaction_failed_url_resolves_transaction_failed_view(self):
        url = reverse("transaction_failed")
        self.assertEqual(resolve(url).func, transaction_failed)
