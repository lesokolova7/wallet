from django import forms
from .models import Wallet


class CreateWallet(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ["type", "currency"]


class TransactionForm(forms.Form):
    receiver = forms.ModelChoiceField(queryset=Wallet.objects.none())
    amount = forms.DecimalField()

    def __init__(self, sender_currency, sender_id, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['receiver'].queryset = Wallet.objects.filter(currency=sender_currency).exclude(pk=sender_id)
