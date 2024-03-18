"""
Helpers module
"""
import string
import random

from wallet.models import Wallet
from wallet_proj.settings import LENGTH_WALLET_NAME


def get_wallet_name(length=LENGTH_WALLET_NAME):
    """
    A unique wallet name generator

    Args:
            length: int
    Returns:
            unique_name: str
    """
    characters = string.ascii_uppercase + string.digits
    wallet_name = ''.join(random.choice(characters) for _ in range(length))
    try:
        Wallet.objects.get(name=wallet_name)
    except Wallet.DoesNotExist:
        return wallet_name
