# Generated by Django 4.2.10 on 2024-03-03 13:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="WalletUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                (
                    "user_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Wallet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(default="GCQ4OA81", max_length=8, unique=True),
                ),
                (
                    "type",
                    models.TextField(
                        choices=[("Visa", "Visa"), ("Mastercard", "Mastercard")]
                    ),
                ),
                (
                    "currency",
                    models.TextField(
                        choices=[("USD", "USD"), ("EUR", "EUR"), ("RUB", "RUB")]
                    ),
                ),
                ("balance", models.DecimalField(decimal_places=2, max_digits=20)),
                ("created_on", models.DateTimeField()),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wallet.walletuser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "transfer_amount",
                    models.DecimalField(decimal_places=2, max_digits=20),
                ),
                ("commission", models.DecimalField(decimal_places=2, max_digits=20)),
                ("status", models.BooleanField()),
                ("timestamp", models.DateTimeField()),
                (
                    "receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wallet_of_receiver",
                        to="wallet.wallet",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wallet_of_sender",
                        to="wallet.wallet",
                    ),
                ),
            ],
        ),
    ]