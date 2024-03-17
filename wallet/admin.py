from django.contrib import admin
from wallet.models import WalletUser, Wallet, Transaction

# Register your models here.
admin.site.register(WalletUser)
admin.site.register(Wallet)
admin.site.register(Transaction)
