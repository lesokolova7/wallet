# Generated by Django 4.2.10 on 2024-03-15 09:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wallet", "0005_alter_wallet_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="transaction",
            old_name="transfer_amount",
            new_name="amount",
        ),
        migrations.AlterField(
            model_name="transaction",
            name="timestamp",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="wallet",
            name="created_on",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="wallet",
            name="name",
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
