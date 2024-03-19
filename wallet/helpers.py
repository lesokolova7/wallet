"""
Helpers module
"""
import string
import random

from django.core.exceptions import ObjectDoesNotExist

from wallet.models import Wallet
from django.conf import settings


def get_wallet_name(length=settings.LENGTH_WALLET_NAME):
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
    except ObjectDoesNotExist:
        return wallet_name
