from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from wallet_proj.settings import MAX_USER_WALLETS_COUNT, INIT_WALLET_CURRENCY_RUB, INIT_WALLET_CURRENCY_FOREIGN, \
    COMMISSION_FREE, COMMISSION, STATUS_SUCCESS, STATUS_FAILURE
from .forms import CreateWallet, TransactionForm
from .helpers import get_wallet_name
from .models import Transaction, Wallet, WalletCurrency
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, get_object_or_404


@login_required(login_url="/login")
def home(request):
    """
    Only the wallets of the current authorized user will be displayed on the home page
    """
    user_wallets = Wallet.objects.filter(user_id=request.user.id)
    user_transactions = Transaction.objects.filter(sender__user_id=request.user.id)
    return render(request, "main/home.html", {"user_wallets": user_wallets, 'user_transactions': user_transactions})


@login_required(login_url="/login")
def delete_wallet(request, wallet_id: int):
    """
    Checking the user's wallet and deleting it
    """
    if request.method == "POST":
        wallet = get_object_or_404(Wallet, id=wallet_id)
        wallet.delete()
        return redirect("/home")


def sign_up(request):
    """
    Creating a new user
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/home")
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {"form": form})


@login_required(login_url="/login")
def create_wallet(request):

    # limit on the number of user wallets
    user_wallets_count = Wallet.objects.filter(user_id=request.user.id).count()

    if user_wallets_count >= MAX_USER_WALLETS_COUNT:
        messages.error(request, "You can't create more than 5 wallets.")
        return redirect("/home")

    if request.method == "POST":
        form = CreateWallet(request.POST)
        if form.is_valid():
            wallet = form.save(commit=False)
            user = User.objects.get(pk=request.user.id)
            wallet.user_id = user.id
            wallet.name = get_wallet_name()

            # deposit accrual depending on the selected currency
            if wallet.currency == WalletCurrency.ruble.value:
                wallet.balance = INIT_WALLET_CURRENCY_RUB
            else:
                wallet.balance = INIT_WALLET_CURRENCY_FOREIGN
            wallet.save()
            return redirect("/home")
    else:
        form = CreateWallet()
    return render(request, "main/create_wallet.html", {"form": form})


@login_required(login_url="/login")
def make_transaction(request, sender_wallet_name: str):
    sender_wallet_user = User.objects.get(pk=request.user.id)
    sender_wallet = Wallet.objects.get(name=sender_wallet_name)
    sender_id = sender_wallet.id
    sender_currency = sender_wallet.currency
    form = TransactionForm(sender_currency, sender_id, request.POST)

    if request.method == 'POST':
        form = TransactionForm(sender_currency, sender_id, request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['receiver']
            amount = form.cleaned_data['amount']

            # calculation of the commission
            if sender_wallet_user == receiver.user:
                commission = Decimal(COMMISSION_FREE)
            else:
                commission = amount * Decimal(COMMISSION)

            # checking balance
            if sender_wallet.balance >= amount + commission:
                sender_wallet.balance -= amount + commission
                sender_wallet.save()

                receiver.balance += amount
                receiver.save()

                status = STATUS_SUCCESS
                redirect_link = "transaction_success"

                messages.success(request, "Transaction successful")
            else:
                status = STATUS_FAILURE
                redirect_link = "transaction_failed"

                messages.error(request, "Insufficient funds for this transaction.")

            Transaction.objects.create(
                sender=sender_wallet,
                receiver=receiver,
                amount=amount,
                commission=commission,
                status=status
            )

            return redirect(redirect_link)

    return render(request, 'main/transaction.html', {"form": form, "sender_wallet_name": sender_wallet_name})


def transaction_success(request):
    return render(request, 'main/transaction_success.html')


def transaction_failed(request):
    return render(request, 'main/transaction_failed.html')

